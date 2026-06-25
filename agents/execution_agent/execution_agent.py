import os
import sys
import time
import subprocess
from pathlib import Path

# -----------------------------------------
# Project Root
# -----------------------------------------

project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

# -----------------------------------------
# Agents
# -----------------------------------------

from agents.report_agent.report_agent import ReportAgent
from agents.failure_agent.failure_agent import FailureAnalysisAgent
from agents.self_healing_agent.self_healing_agent import SelfHealingAgent
from agents.retry_agent.retry_agent import RetryAgent

class ExecutionAgent:

    def __init__(self, project_root):
        self.project_root = Path(project_root)

    def run_behave(self, feature_name=None):

        # -----------------------------------------
        # Decide which feature(s) to execute
        # -----------------------------------------

        if feature_name:

            feature_path = (
                self.project_root
                / "framework"
                / "features"
                / f"{feature_name}.feature"
            )

            if not feature_path.exists():
                raise FileNotFoundError(
                    f"Feature file not found:\n{feature_path}"
                )

            test_name = feature_name

        else:

            feature_path = (
                self.project_root
                / "framework"
                / "features"
            )

            test_name = "Complete Test Suite"

        print("\nRunning Tests...\n")

        start_time = time.time()

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "behave",
                str(feature_path)
            ],
            cwd=self.project_root,
            env={
                **os.environ,
                "PYTHONPATH": str(self.project_root)
            },
            capture_output=True,
            text=True
        )

        execution_time = round(
            time.time() - start_time,
            2
        )

        print(result.stdout)

        if result.stderr:
            print(result.stderr)

        status = (
            "PASS"
            if result.returncode == 0
            else "FAIL"
        )

        error_type = "N/A"
        root_cause = "N/A"
        suggested_fix = "N/A"

        # -----------------------------------------
        # Failure Analysis
        # -----------------------------------------

        if status == "FAIL":

            failure_agent = FailureAnalysisAgent()

            analysis = failure_agent.analyze(
                result.stdout + result.stderr
            )

            error_type = analysis.get(
                "error_type",
                "N/A"
            )

            root_cause = analysis.get(
                "root_cause",
                "N/A"
            )

            suggested_fix = analysis.get(
                "suggested_fix",
                "N/A"
            )

            failure_agent.save_analysis(
                self.project_root,
                analysis
            )

            # -----------------------------------------
            # Self Healing
            # -----------------------------------------

            page_file = (
                self.project_root
                / "framework"
                / "pages"
                / f"{test_name}_page.py"
            )

            healing_agent = SelfHealingAgent()

            healing_result = healing_agent.suggest_locator_fixes(
                page_file
            )

            healing_agent.save_healing_report(
                self.project_root,
                healing_result
            )
            retry_agent = RetryAgent()

            retry_status = retry_agent.retry_test(
                self.project_root,
                test_name
            )

            print(f"\nRetry Status : {retry_status}")
        # -----------------------------------------
        # Report
        # -----------------------------------------

        report_agent = ReportAgent(
            self.project_root
        )

        report_agent.generate_report(
            test_name=test_name,
            status=status,
            execution_time=f"{execution_time} sec",
            error_type=error_type,
            root_cause=root_cause,
            suggested_fix=suggested_fix
        )

        return result.returncode


# -----------------------------------------
# Main
# -----------------------------------------

if __name__ == "__main__":

    project_root = (
        Path(__file__)
        .resolve()
        .parents[2]
    )

    feature_name = None

    if len(sys.argv) > 1:
        feature_name = sys.argv[1]

    agent = ExecutionAgent(
        project_root
    )

    agent.run_behave(feature_name)