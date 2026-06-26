from pathlib import Path
import json
import re


class SelfHealingAgent:

    def __init__(self):
        pass

    # ----------------------------------------
    # Extract all locators from page object
    # ----------------------------------------

    def extract_locators(self, page_file):

        with open(page_file, "r", encoding="utf-8") as f:
            content = f.read()

        pattern = r'By\.(XPATH|CSS_SELECTOR|ID|NAME|CLASS_NAME|LINK_TEXT)\s*,\s*"([^"]+)"'

        matches = re.findall(pattern, content)

        locators = []

        for locator_type, locator in matches:

            locators.append({

                "type": locator_type,

                "locator": locator

            })

        return locators
    
    def extract_failed_method(self, error_text):


        # Extract method name from stacktrace
        match = re.search(r'File ".*?_page\.py".*?in (\w+)', error_text, re.DOTALL)

        if match:
            return match.group(1)

        return None
    def find_locator_in_method(
    self,
    page_file,
    method_name
):

        with open(page_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Find the complete method body
        method_pattern = (
            rf"def {method_name}\(.*?\):(.*?)(?=\n\s*def |\Z)"
        )

        method_match = re.search(
            method_pattern,
            content,
            re.DOTALL
        )

        if not method_match:
            return None

        method_body = method_match.group(1)

        locator_pattern = (
            r'By\.(XPATH|CSS_SELECTOR|ID|NAME|CLASS_NAME|LINK_TEXT)\s*,\s*"([^"]+)"'
        )

        locator_match = re.search(
            locator_pattern,
            method_body
        )

        if locator_match:

            return {

                "type": locator_match.group(1),

                "locator": locator_match.group(2)

            }

        return None
    # ----------------------------------------
    # Find failed locator
    # ----------------------------------------

    def find_failed_locator(
        self,
        error_text,
        page_file
    ):

        locators = self.extract_locators(page_file)

        # V2
        # Currently returns first locator.
        # V3 will map stacktrace -> method -> locator.

        if locators:

            return locators[0]

        return None

    # ----------------------------------------
    # Generate healing suggestions
    # ----------------------------------------

    def suggest_locator_fixes(
        self,
        failed_locator
    ):

        suggestions = []

        locator = failed_locator["locator"]

        if "text()" in locator:

            try:

                text_value = (

                    locator

                    .split("text()='")[1]

                    .split("'")[0]

                )

            except Exception:

                text_value = ""

            suggestions.append(

                f"//*[contains(text(),'{text_value}')]"

            )

            suggestions.append(

                f"//button[contains(text(),'{text_value}')]"

            )

            suggestions.append(

                f"//div[contains(text(),'{text_value}')]"

            )

            suggestions.append(

                f"//span[contains(text(),'{text_value}')]"

            )

        return {

            "locator_type": failed_locator["type"],

            "original_locator": locator,

            "suggestions": suggestions

        }

    # ----------------------------------------
    # Complete healing workflow
    # ----------------------------------------

    def analyze_failure(
        self,
        error_text,
        page_file
    ):

        method_name = self.extract_failed_method(
            error_text
        )

        print(f"\nFailed Method : {method_name}")

        failed_locator = self.find_locator_in_method(
            page_file,
            method_name
        )

        if failed_locator is None:

            return {

                "status": "NO_LOCATOR_FOUND"

            }

        return self.suggest_locator_fixes(

            failed_locator

        )

    # ----------------------------------------
    # Save report
    # ----------------------------------------

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


if __name__ == "__main__":

    project_root = (

        Path(__file__)

        .resolve()

        .parents[2]

    )

    page_file = (

        project_root

        / "framework"

        / "pages"

        / "button_click_page.py"

    )

    sample_error = "TimeoutException"

    agent = SelfHealingAgent()

    result = agent.analyze_failure(

        sample_error,

        page_file

    )

    agent.save_healing_report(

        project_root,

        result

    )