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

        if "TimeoutException" in error_text:

            analysis["error_type"] = "TimeoutException"

            analysis["root_cause"] = (
                "Element was not found within timeout period"
            )

            analysis["suggested_fix"] = (
                "Verify locator and page load timing"
            )

            analysis["confidence"] = 0.90

        elif "NoSuchElementException" in error_text:

            analysis["error_type"] = "NoSuchElementException"

            analysis["root_cause"] = (
                "Locator does not match any element"
            )

            analysis["suggested_fix"] = (
                "Update locator strategy"
            )

            analysis["confidence"] = 0.95

        elif "AssertionError" in error_text:

            analysis["error_type"] = "AssertionError"

            analysis["root_cause"] = (
                "Actual result differs from expected result"
            )

            analysis["suggested_fix"] = (
                "Review validation logic"
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

