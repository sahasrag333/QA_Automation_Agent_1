import subprocess
from pathlib import Path
import sys

class OrchestratorAgent:


    def __init__(self):

        self.project_root = (
            Path(__file__)
            .resolve()
            .parents[2]
        )



    def run(self, test_name):

            
            print(f"\nProcessing: {test_name}\n")

            feature_file = (
                self.project_root /
                "framework" /
                "features" /
                f"{test_name}.feature"
            )

            page_file = (
                self.project_root /
                "framework" /
                "pages" /
                f"{test_name}_page.py"
            )

            step_file = (
                self.project_root /
                "framework" /
                "features" /
                "steps" /
                f"{test_name}_steps.py"
            )

            # -------------------------
            # BDD Generation
            # -------------------------

            if not feature_file.exists():

                print(
                    "\nSTEP 1 : Generating Feature File"
                )

                subprocess.run(
                    [
                        sys.executable,
                        "agents/bdd_agent/bdd_agent.py",
                        test_name
                    ]
                )

            else:

                print(
                    "\nSTEP 1 : Feature File Exists - Skipping"
                )

            # -------------------------
            # Code Generation
            # -------------------------

            if (
                not page_file.exists()
                or
                not step_file.exists()
            ):

                print(
                    "\nSTEP 2 : Generating Automation Code"
                )

                subprocess.run(
                    [
                        sys.executable,
                        "agents/code_agent/code_agent.py",
                        test_name
                    ]
                )

            else:

                print(
                    "\nSTEP 2 : Automation Code Exists - Skipping"
                )

            # -------------------------
            # Execution
            # -------------------------

            print(
                "\nSTEP 3 : Executing Test Suite"
            )

            subprocess.run(
                [
                    sys.executable,
                    "agents/execution_agent/execution_agent.py"
                ]
            )

            print(
                "\nPipeline Completed Successfully"
            )
            


if __name__ == "__main__":


    if len(sys.argv) < 2:

        print(
            "Usage: python orchestrator_agent.py test_name"
        )

        sys.exit(1)

    test_name = sys.argv[1]

    agent = OrchestratorAgent()

    agent.run(test_name)
