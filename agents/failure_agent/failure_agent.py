from pathlib import Path
import json

class FailureAnalysisAgent:


    def analyze(self, error_text):

        

        analysis = {

            "status": "FAIL",

            "error_type": "Unknown",

            "root_cause": "Unknown",

            "suggested_fix": "Manual investigation required",

            "confidence": 0.50,

            "screenshot": None

        }

        # --------------------------------------------------
        # Framework Errors
        # --------------------------------------------------

        if "ImportError" in error_text:

            analysis["error_type"] = "ImportError"

            analysis["root_cause"] = (
                "Invalid Python import detected."
            )

            analysis["suggested_fix"] = (
                "Verify import statements and module paths."
            )

            analysis["confidence"] = 0.99

        elif "ModuleNotFoundError" in error_text:

            analysis["error_type"] = "ModuleNotFoundError"

            analysis["root_cause"] = (
                "Python module could not be located."
            )

            analysis["suggested_fix"] = (
                "Check package structure and import path."
            )

            analysis["confidence"] = 0.99

        elif "SyntaxError" in error_text:

            analysis["error_type"] = "SyntaxError"

            analysis["root_cause"] = (
                "Python syntax error."
            )

            analysis["suggested_fix"] = (
                "Fix generated Python syntax."
            )

            analysis["confidence"] = 0.99

        elif "AttributeError" in error_text:

            analysis["error_type"] = "AttributeError"

            analysis["root_cause"] = (
                "Object does not contain requested attribute."
            )

            analysis["suggested_fix"] = (
                "Verify method and attribute names."
            )

            analysis["confidence"] = 0.98

        elif "NameError" in error_text:

            analysis["error_type"] = "NameError"

            analysis["root_cause"] = (
                "Undefined variable or object."
            )

            analysis["suggested_fix"] = (
                "Verify generated variable names."
            )

            analysis["confidence"] = 0.98

        # --------------------------------------------------
        # Selenium Errors
        # --------------------------------------------------

        elif "TimeoutException" in error_text:

            analysis["error_type"] = "TimeoutException"

            analysis["root_cause"] = (
                "Element was not found within timeout."
            )

            analysis["suggested_fix"] = (
                "Verify locator and page load timing."
            )

            analysis["confidence"] = 0.90

        elif "NoSuchElementException" in error_text:

            analysis["error_type"] = "NoSuchElementException"

            analysis["root_cause"] = (
                "Locator did not match any element."
            )

            analysis["suggested_fix"] = (
                "Update locator strategy."
            )

            analysis["confidence"] = 0.95

        elif "StaleElementReferenceException" in error_text:

            analysis["error_type"] = "StaleElementReferenceException"

            analysis["root_cause"] = (
                "DOM changed before interaction."
            )

            analysis["suggested_fix"] = (
                "Re-locate the element before interacting."
            )

            analysis["confidence"] = 0.90

        # --------------------------------------------------
        # Assertion
        # --------------------------------------------------

        elif "AssertionError" in error_text:

            analysis["error_type"] = "AssertionError"

            analysis["root_cause"] = (
                "Expected result does not match actual result."
            )

            analysis["suggested_fix"] = (
                "Review validation logic."
            )

            analysis["confidence"] = 0.85

        return analysis

    def save_analysis(self, project_root, analysis, screenshot_path=None):
        analysis["screenshot"] = screenshot_path

        output_dir = Path(project_root) / "framework" / "reports"
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / "failure_analysis.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=4)

        print(f"\nFailure Analysis Saved:\n{output_file}")
       
    
if __name__ == "__main__":


    sample_error = """
    selenium.common.exceptions.TimeoutException
    """

    project_root = (
        Path(__file__)
        .resolve()
        .parents[2]
    )

    agent = FailureAnalysisAgent()

    result = agent.analyze(
        sample_error
    )

    agent.save_analysis(
        project_root,
        result
    )

