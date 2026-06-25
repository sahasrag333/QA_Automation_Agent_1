from pathlib import Path
import json
import re
class SelfHealingAgent:

    def __init__(self):
        pass

    def suggest_locator_fixes(
        self,
        locator
    ):
        suggestions = []

        if "text()" in locator:

            text_value = (
                locator
                .split("text()='")[1]
                .split("'")[0]
            )

            suggestions.append(
                f"//*[contains(text(),'{text_value}')]"
            )

            suggestions.append(
                f"//button[contains(text(),'{text_value}')]"
            )

            suggestions.append(
                f"//div[contains(text(),'{text_value}')]"
            )

        return {
            "original_locator": locator,
            "suggestions": suggestions
        }

    def save_healing_report(
        self,
        project_root,
        result
    ):

        output_file = (
            Path(project_root)
            / "framework"
            / "reports"
            / "healing_report.json"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                result,
                f,
                indent=4
            )

        print(
            f"\nHealing Report Saved:\n{output_file}"
        )



    def extract_locators(self, page_file):

        with open(page_file, "r", encoding="utf-8") as f:
            content = f.read()

        pattern = r'By\.(XPATH|CSS_SELECTOR|ID|NAME|CLASS_NAME|LINK_TEXT)\s*,\s*"([^"]+)"'

        matches = re.findall(pattern, content)

        locators = []

        for locator_type, locator in matches:

            locators.append(
                {
                    "type": locator_type,
                    "locator": locator
                }
            )

        return locators
if __name__ == "__main__":


    locator = (
        "//h5[text()='Elements']"
    )

    project_root = (
        Path(__file__)
        .resolve()
        .parents[2]
    )

    agent = SelfHealingAgent()

    result = (
        agent.suggest_locator_fixes(
            locator
        )
    )

    agent.save_healing_report(
        project_root,
        result
    )
