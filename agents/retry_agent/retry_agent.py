import json
import subprocess
import sys
import os
from pathlib import Path


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

        # -----------------------------
        # Display suggestions
        # -----------------------------

        if "locators" in healing_data:

            for locator in healing_data["locators"]:

                print(
                    f"Original Locator : {locator['original']}"
                )

                suggestions = locator.get(
                    "suggestions",
                    []
                )

                if suggestions:

                    print(
                        "Suggested Locator :",
                        suggestions[0]
                    )

                print()

        else:

            print(healing_data)

        # -----------------------------
        # Retry Execution
        # -----------------------------

        feature_file = (
            project_root
            / "framework"
            / "features"
            / f"{feature_name}.feature"
        )

        print(
            f"Retrying Feature : {feature_name}\n"
        )

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

        print(result.stdout)

        if result.stderr:

            print(result.stderr)

        if result.returncode == 0:

            print("\nRetry Result : PASS\n")

            return "PASS"

        print("\nRetry Result : FAIL\n")

        return "FAIL"


if __name__ == "__main__":

    project_root = (
        Path(__file__)
        .resolve()
        .parents[2]
    )

    agent = RetryAgent()

    agent.retry_test(
        project_root,
        "button_click"
    )