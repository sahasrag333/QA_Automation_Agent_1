import os
import sys
import time
import subprocess
from pathlib import Path

# --------------------------------------------------
# Project Root
# --------------------------------------------------

project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

# --------------------------------------------------
# Agents
# --------------------------------------------------

from agents.validation_agent.validation_agent import ValidationAgent
from agents.failure_agent.failure_agent import FailureAnalysisAgent
from agents.self_healing_agent.self_healing_agent import SelfHealingAgent
from agents.retry_agent.retry_agent import RetryAgent
from agents.report_agent.report_agent import ReportAgent


class ExecutionAgent:

    MAX_HEALING_ATTEMPTS = 5

    FRAMEWORK_ERRORS = [

        "ImportError",

        "ModuleNotFoundError",

        "SyntaxError",

        "AttributeError",

        "AmbiguousStep",

        "UndefinedStep",

        "ValidationError"

    ]

    def __init__(self, project_root):

        self.project_root = Path(project_root)

        self.healing_history = []

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------

    def validate_generated_code(
        self,
        feature_name
    ):

        validator = ValidationAgent()

        feature_file = (
            self.project_root
            / "framework"
            / "features"
            / f"{feature_name}.feature"
        )

        page_file = (

                self.project_root

                / "framework"

                / "pages"

                / f"{feature_name}_page.py"

            )

        step_file = (
            self.project_root
            / "framework"
            / "features"
            / "steps"
            / f"{feature_name}_steps.py"
        )

        common_step_file = (
            self.project_root
            / "framework"
            / "features"
            / "steps"
            / "common_steps.py"
        )

        feature_steps = validator.extract_feature_steps(
            feature_file
        )

        step_definitions = validator.extract_step_definitions(
            common_step_file,
            step_file
        )

        step_validation = validator.validate_steps(
            feature_steps,
            step_definitions
        )

        method_validation = validator.validate_page_methods(
            step_file,
            page_file
        )

        import_validation = validator.validate_imports(
            step_file,
            page_file
        )

        duplicate_validation = validator.validate_duplicate_steps(
            step_definitions
        )

        report = {

            "step_validation": step_validation,

            "method_validation": method_validation,

            "import_validation": import_validation,

            "duplicate_validation": duplicate_validation

        }

        validator.save_validation_report(
            self.project_root,
            report
        )

        return report

    # --------------------------------------------------
    # Execute Behave
    # --------------------------------------------------

    def execute_behave(
        self,
        feature_path
    ):

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

        return {

            "status": status,

            "stdout": result.stdout,

            "stderr": result.stderr,

            "execution_time": execution_time

        }

    # --------------------------------------------------
    # Failure Analysis
    # --------------------------------------------------

    def analyze_failure(
        self,
        output
    ):

        failure_agent = FailureAnalysisAgent()

        analysis = failure_agent.analyze(
            output
        )

        failure_agent.save_analysis(
            self.project_root,
            analysis
        )

        return analysis

    # --------------------------------------------------
    # Self Healing
    # --------------------------------------------------

    def perform_self_healing(
        self,
        output,
        page_file
    ):

        healing_agent = SelfHealingAgent()

        healing_result = healing_agent.analyze_failure(
            output,
            page_file
        )

        healing_agent.save_healing_report(
            self.project_root,
            healing_result
        )

        return healing_result

    # --------------------------------------------------
    # Retry
    # --------------------------------------------------

    def retry_execution(
        self,
        feature_name
    ):

        retry_agent = RetryAgent()

        return retry_agent.retry_test(
            self.project_root,
            feature_name
        )
    
        # --------------------------------------------------
    # Healing Loop
    # --------------------------------------------------

    def healing_loop(
        self,
        feature_name,
        page_file,
        execution_result
    ):

        status = execution_result["status"]

        output = (
            execution_result["stdout"]
            +
            execution_result["stderr"]
        )

        error_type = "N/A"
        root_cause = "N/A"
        suggested_fix = "N/A"

        attempt = 0

        while (

            status == "FAIL"

            and

            attempt < self.MAX_HEALING_ATTEMPTS

        ):

            attempt += 1

            print()

            print("=" * 60)

            print(f"HEALING ATTEMPT : {attempt}")

            print("=" * 60)

            print(f"Current Status : {status}")

            print(
                f"Attempt : {attempt}/{self.MAX_HEALING_ATTEMPTS}"
            )

            # ---------------------------------
            # Failure Analysis
            # ---------------------------------

            analysis = self.analyze_failure(
                output
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

            # ---------------------------------
            # Skip Framework Errors
            # ---------------------------------

            if error_type in self.FRAMEWORK_ERRORS:

                print()

                print("Framework Error Detected.")

                print("Stopping Healing Loop.")

                break

            # ---------------------------------
            # Self Healing
            # ---------------------------------

            self.perform_self_healing(
                output,
                page_file
            )

            # ---------------------------------
            # Retry
            # ---------------------------------

            retry_result = self.retry_execution(
                feature_name
            )

            self.healing_history.append(

                {

                    "attempt": attempt,

                    "status": retry_result["status"],

                    "error_type": error_type,

                    "root_cause": root_cause

                }

            )

            print()

            print(
                f"Retry Status : {retry_result['status']}"
            )

            # ---------------------------------
            # Success
            # ---------------------------------

            if retry_result["status"] == "PASS":

                status = "PASS"

                print()

                print("Healing Successful.")

                break

            # ---------------------------------
            # Continue with next retry
            # ---------------------------------

            output = (

                retry_result["stdout"]

                +

                retry_result["stderr"]

            )

            status = "FAIL"

        result = {

            "status": status,

            "error_type": error_type,

            "root_cause": root_cause,

            "suggested_fix": suggested_fix

        }

        print()

        print("=" * 60)

        print("Healing Loop Finished")

        print(result)

        print("=" * 60)

        return result
    

        # --------------------------------------------------
    # Run Behave
    # --------------------------------------------------

    def run_behave(self, feature_name=None):

        # -----------------------------------------
        # Decide Feature
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

        # -----------------------------------------
        # Validation
        # -----------------------------------------

        if feature_name:

            print()

            print("=" * 60)

            print("RUNNING VALIDATION")

            print("=" * 60)

            validation = self.validate_generated_code(
                feature_name
            )

            validation_failed = (

                validation["step_validation"]["status"] == "FAIL"

                or

                validation["method_validation"]["status"] == "FAIL"

                or

                validation["import_validation"]["status"] == "FAIL"

                or

                validation["duplicate_validation"]["status"] == "FAIL"

            )

            if validation_failed:

                print()

                print("Validation Failed.")

                report_agent = ReportAgent(
                    self.project_root
                )

                report_agent.generate_report(

                    test_name=test_name,

                    status="VALIDATION FAILED",

                    execution_time="0 sec",

                    error_type="ValidationError",

                    root_cause="Generated code validation failed.",

                    suggested_fix="Check validation_report.json",

                    healing_history=[]

                )

                return "VALIDATION FAILED"

            print()

            print("Validation Passed.")

        # -----------------------------------------
        # Execute Test
        # -----------------------------------------

        execution_result = self.execute_behave(
            feature_path
        )

        status = execution_result["status"]

        error_type = "N/A"

        root_cause = "N/A"

        suggested_fix = "N/A"

        # -----------------------------------------
        # Failure Handling
        # -----------------------------------------

        if status == "FAIL":

            analysis = self.analyze_failure(

                execution_result["stdout"]

                +

                execution_result["stderr"]

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

            # -----------------------------------------
            # Skip Healing
            # -----------------------------------------

            if error_type in self.FRAMEWORK_ERRORS:

                print()

                print("=" * 60)

                print("FRAMEWORK ERROR DETECTED")

                print("=" * 60)

                print(f"Error Type : {error_type}")

                print()

                print("Self-Healing Skipped.")

            else:

                page_file = (

                    self.project_root

                    / "framework"

                    / "pages"

                    / f"{test_name}_page.py"

                )

                healing_result = self.healing_loop(

                    test_name,

                    page_file,

                    execution_result

                )

                status = healing_result["status"]

                error_type = healing_result["error_type"]

                root_cause = healing_result["root_cause"]

                suggested_fix = healing_result["suggested_fix"]

    
            # -----------------------------------------
        # Generate Report
        # -----------------------------------------

        report_agent = ReportAgent(
            self.project_root
        )

        report_agent.generate_report(

            test_name=test_name,

            status=status,

            execution_time=f"{execution_result['execution_time']} sec",

            error_type=error_type,

            root_cause=root_cause,

            suggested_fix=suggested_fix,

            healing_history=self.healing_history

        )

        return status


# --------------------------------------------------
# Main
# --------------------------------------------------

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

    final_status = agent.run_behave(
        feature_name
    )

    print()

    print("=" * 60)

    print(f"FINAL RESULT : {final_status}")

    print("=" * 60)