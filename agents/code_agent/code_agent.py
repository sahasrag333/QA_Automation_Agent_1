from pathlib import Path
import sys
import re

project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from agents.utils.llm import generate

recordings_dir = project_root / "framework" / "recordings"

features_dir = (
    project_root /
    "framework" /
    "features"
)

pages_dir = (
    project_root /
    "framework" /
    "pages"
)

steps_dir = (
    project_root /
    "framework" /
    "step_definitions"
)

tests_dir = (
    project_root /
    "framework" /
    "tests"
)

pages_dir.mkdir(parents=True, exist_ok=True)
steps_dir.mkdir(parents=True, exist_ok=True)
tests_dir.mkdir(parents=True, exist_ok=True)

# --------------------------
# Select File
# --------------------------

if len(sys.argv) > 1:
    base_name = sys.argv[1]
else:
    feature_files = sorted(
        features_dir.glob("*.feature")
    )

    if not feature_files:
        raise FileNotFoundError(
            "No feature files found."
        )

    base_name = feature_files[0].stem
    print(base_name)

recording_file = (
    recordings_dir /
    f"{base_name}.py"
)

feature_file = (
    features_dir /
    f"{base_name}.feature"
)

if not recording_file.exists():
    raise FileNotFoundError(
        recording_file
    )

if not feature_file.exists():
    raise FileNotFoundError(
        feature_file
    )

playwright_code = recording_file.read_text(
    encoding="utf-8"
)

feature_content = feature_file.read_text(
    encoding="utf-8"
)

# --------------------------
# Prompt
# --------------------------
prompt = f"""
You are a Senior QA Automation Architect.

Generate production-ready Selenium Python automation framework code.

Framework Stack:

* Python
* Selenium
* Behave
* Page Object Model
* Explicit Waits

Project Structure:

framework/
│
├── config/
│   └── config.py
│
├── utils/
│   ├── driver_factory.py
│   └── logger.py
│
├── pages/
├── step_definitions/
├── tests/
├── reports/

IMPORTANT RULES:

1. NEVER create webdriver.Chrome() directly.

Always use:

from framework.utils.driver_factory import DriverFactory

Example:

driver = DriverFactory.get_driver()

---

2. NEVER hardcode URLs.

Always use:

from framework.config.config import BASE_URL

Example:

driver.get(BASE_URL)

---

3. ALWAYS use logging.

Import:

from framework.utils.logger import get_logger

Example:

logger = get_logger(**name**)

logger.info("Opening application")

---

4. Use explicit waits.

Never use:

time.sleep()

---

5. Create reusable Page Object methods.

---

6. Generate proper imports.

---

7. Use the Playwright recording to infer locators.

---

8. Use the Feature File to infer business behavior.

---

9. Step definitions must use Behave decorators.

---

10. Return ONLY the output below.

===PAGE_OBJECT=== <python code>

===STEP_DEFINITIONS=== <python code>

===TEST_FILE=== <python code>

Feature File:

{feature_content}

Playwright Recording:

{playwright_code}

IMPORTANT:

Generate code that is internally consistent.

1. Every imported class in STEP_DEFINITIONS must exist in PAGE_OBJECT.

2. Every method called in STEP_DEFINITIONS must exist in PAGE_OBJECT.

3. Do not generate undefined classes.

4. Use DriverFactory.get_driver().

5. Do not use __init__(driver).

6. Validate all references before returning code.
"""
response = generate( prompt=prompt, task_type="code" )
# --------------------------
# Parse Response
# --------------------------
page_match = re.search(
    r"(?:===PAGE_OBJECT===|### PAGE_OBJECT)\s*(.*?)\s*(?:===STEP_DEFINITIONS===|### STEP_DEFINITIONS)",
    response,
    re.DOTALL
)

step_match = re.search(
    r"(?:===STEP_DEFINITIONS===|### STEP_DEFINITIONS)\s*(.*?)\s*(?:===TEST_FILE===|### TEST_FILE)",
    response,
    re.DOTALL
)

test_match = re.search(
    r"(?:===TEST_FILE===|### TEST_FILE)\s*(.*)",
    response,
    re.DOTALL
)

if not (
    page_match and
    step_match and
    test_match
):
    print("\n========== LLM RESPONSE ==========\n")
    print(response)
    print("\n========== END RESPONSE ==========\n")

    raise Exception(
        "Unable to parse model response."
    )

page_code = page_match.group(1).strip()
step_code = step_match.group(1).strip()
test_code = test_match.group(1).strip()
def clean_code(code):
    code = code.replace("```python", "")
    code = code.replace("```", "")
    return code.strip()

page_code = clean_code(page_code)
step_code = clean_code(step_code)
test_code = clean_code(test_code)
# --------------------------
# Save Files
# --------------------------

page_file = (
    pages_dir /
    f"{base_name}_page.py"
)

step_file = (
    steps_dir /
    f"{base_name}_steps.py"
)

test_file = (
    tests_dir /
    f"test_{base_name}.py"
)

page_file.write_text(
    page_code,
    encoding="utf-8"
)

step_file.write_text(
    step_code,
    encoding="utf-8"
)

test_file.write_text(
    test_code,
    encoding="utf-8"
)

print("\nFiles Generated Successfully\n")

print(page_file)
print(step_file)
print(test_file)