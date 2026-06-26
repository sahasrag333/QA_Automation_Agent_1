import json
import subprocess
import sys
import os
from pathlib import Path

from agents.healing_engine.healing_engine import HealingEngine


class RetryAgent:

    def retry_test(self, project_root, feature_name):

        project_root = Path(project_root)

        report_file = (
            project_root
            / "framework"
            / "reports"
            / "healing_report.json"
        )

        if not report_file.exists():

            print("\nHealing report not found.")

            return "FAIL"

        with open(
            report_file,
            "r",
            encoding="utf-8"
        ) as f:

            healing_data = json.load(f)

        print("\n========== RETRY AGENT ==========\n")

        print("Healing Suggestions:\n")

        print(healing_data)

        feature_file = (
            project_root
            / "framework"
            / "features"
            / f"{feature_name}.feature"
        )

        print(f"\nRetrying Feature : {feature_name}")

        # --------------------------------------------------
        # Healing Engine
        # --------------------------------------------------

        engine = HealingEngine()

        temp_file = engine.apply_first_fix(
            project_root,
            feature_name
        )

        # ---------------------------------------
# No healing possible
# ---------------------------------------

        if temp_file is None:

            print("\nNo healing could be applied.")

            return {

                "status": "FAIL",

                "stdout": "",

                "stderr": "No locator available for healing."

            }


        page_file = (
            project_root
            / "framework"
            / "pages"
            / f"{feature_name}_page.py"
        )

        backup_file = engine.backup_original_page(
            page_file
        )

        try:

            engine.apply_healed_page(
                temp_file,
                page_file
            )

            print("\nRunning Retry...\n")

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "behave",
                    str(feature_file)
                ],
                cwd=project_root,
                env={
                    **os.environ,
                    "PYTHONPATH": str(project_root)
                },
                capture_output=True,
                text=True
            )

        finally:

            engine.restore_original_page(
                backup_file,
                page_file
            )

            engine.cleanup_temp_page(
                temp_file
            )

        print(result.stdout)

        if result.stderr:

            print(result.stderr)

        retry_result = {

            "status": (
                "PASS"
                if result.returncode == 0
                else "FAIL"
            ),

            "stdout": result.stdout,

            "stderr": result.stderr

        }

        print(
            f"\nRetry Result : {retry_result['status']}\n"
        )

        return retry_result


if __name__ == "__main__":

    project_root = (
        Path(__file__)
        .resolve()
        .parents[2]
    )

    agent = RetryAgent()

    agent.retry_test(
        project_root,
        "widget_click"
    )