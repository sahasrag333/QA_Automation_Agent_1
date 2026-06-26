from pathlib import Path
import sys
import re

project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from agents.utils.llm import generate

# ---------------------------------------------------------
# Directories
# ---------------------------------------------------------

recordings_dir = (
    project_root
    / "framework"
    / "recordings"
)

features_dir = (
    project_root
    / "framework"
    / "features"
)

pages_dir = (
    project_root
    / "framework"
    / "pages"
)

# IMPORTANT
# Behave loads steps from here
steps_dir = (
    project_root
    / "framework"
    / "features"
    / "steps"
)

tests_dir = (
    project_root
    / "framework"
    / "tests"
)

pages_dir.mkdir(parents=True, exist_ok=True)
steps_dir.mkdir(parents=True, exist_ok=True)
tests_dir.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------
# Feature Selection
# ---------------------------------------------------------

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

print(f"\nGenerating Code For : {base_name}")

# ---------------------------------------------------------
# Files
# ---------------------------------------------------------

recording_file = (
    recordings_dir
    / f"{base_name}.py"
)

feature_file = (
    features_dir
    / f"{base_name}.feature"
)

if not recording_file.exists():

    raise FileNotFoundError(recording_file)

if not feature_file.exists():

    raise FileNotFoundError(feature_file)

playwright_code = recording_file.read_text(
    encoding="utf-8"
)

feature_content = feature_file.read_text(
    encoding="utf-8"
)

# ---------------------------------------------------------
# Naming Convention
# ---------------------------------------------------------

page_class = "".join(
    word.capitalize()
    for word in base_name.split("_")
) + "Page"

page_file_name = f"{base_name}_page"

# ---------------------------------------------------------
# Prompt
# ---------------------------------------------------------

prompt = f"""
You are a Senior QA Automation Architect.

Generate production-ready Selenium automation code.

Framework Stack

- Python
- Selenium
- Behave
- Page Object Model
- Explicit Waits
PAGE OBJECT REQUIREMENTS

Every generated page object MUST contain these imports exactly:

from framework.utils.driver_factory import DriverFactory
from framework.config.config import BASE_URL
from framework.utils.logger import get_logger

Never omit these imports.

Every page object must obtain the driver using:

driver = DriverFactory.get_driver()

Never use:

webdriver.Chrome()

Never create a local webdriver instance.
================================================

PROJECT RULES

================================================

1.

Never use webdriver.Chrome().

Always use

DriverFactory.get_driver()

================================================

2.

Never hardcode URLs.

Always use BASE_URL.

================================================

3.

Never use time.sleep()

Use Explicit Waits.

================================================

4.

Always use logging.

================================================

5.

Generate ONE page object class.

Class name MUST be

{page_class}

File name MUST be

{page_file_name}.py

================================================

6.

The framework already contains

framework/features/steps/common_steps.py

DO NOT regenerate

Given the demoqa website is open

or any common Given step.

Generate ONLY feature-specific steps.

IMPORTANT

Never import anything from

framework.features.steps.common_steps

Behave automatically discovers all step definitions.

Do NOT generate statements like:

from framework.features.steps.common_steps import ...

Do NOT import any Given, When or Then methods from common_steps.py.

Simply omit common steps from the generated step file.

================================================
14.

IMPORTANT

The step definition decorators MUST exactly match the feature file.

Do NOT paraphrase.

Do NOT shorten.

Do NOT rewrite.

Example:

Feature:

Then the resizable box with restriction is displayed and can be interacted with

Generate exactly:

@then("the resizable box with restriction is displayed and can be interacted with")

Never change it to:

@then("the resizable box with restriction is interacted with")

7.

Never generate

BasePage

HomePage

Generic Page

Always generate

class {page_class}

================================================

8.

Every imported class MUST exist.

Every called method MUST exist.

Every method used in Behave must exist.

================================================

9.

Do not generate duplicate step definitions.

================================================

10.

Return ONLY

===PAGE_OBJECT===

===STEP_DEFINITIONS===

===TEST_FILE===

================================================

Feature File

{feature_content}

================================================

Playwright Recording

{playwright_code}

================================================

Before returning your answer verify

✓ Imports

✓ Class names

✓ Behave decorators

✓ Page methods

✓ Locator consistency

✓ No duplicate steps



15.

Before returning the PAGE_OBJECT code, verify it contains:

from framework.utils.driver_factory import DriverFactory

If this import is missing, regenerate the page object before returning the answer.

"""
response = generate( prompt=prompt, task_type="code" )
    # ---------------------------------------------------------
# Parse Response
# ---------------------------------------------------------

page_match = re.search(
    r"(?:===PAGE_OBJECT===|### PAGE_OBJECT)\s*(.*?)\s*(?:===STEP_DEFINITIONS===|### STEP_DEFINITIONS)",
    response,
    re.DOTALL,
)

step_match = re.search(
    r"(?:===STEP_DEFINITIONS===|### STEP_DEFINITIONS)\s*(.*?)\s*(?:===TEST_FILE===|### TEST_FILE)",
    response,
    re.DOTALL,
)

test_match = re.search(
    r"(?:===TEST_FILE===|### TEST_FILE)\s*(.*)",
    response,
    re.DOTALL,
)

if not (page_match and step_match and test_match):

    print("\n========== RAW LLM RESPONSE ==========\n")
    print(response)
    print("\n======================================\n")

    raise Exception(
        "Unable to parse model response."
    )

# ---------------------------------------------------------
# Clean Code
# ---------------------------------------------------------

def clean_code(code):

    code = code.replace("```python", "")
    code = code.replace("```", "")

    return code.strip()


page_code = clean_code(page_match.group(1))
required_import = "from framework.utils.driver_factory import DriverFactory"

if required_import not in page_code:

    page_code = (
        required_import
        + "\n"
        + page_code
    )
step_code = clean_code(step_match.group(1))
# ---------------------------------------------------------
# Fix page imports automatically
# ---------------------------------------------------------

step_code = re.sub(
    r"from\s+\w+_page\s+import",
    f"from framework.pages.{page_file_name} import",
    step_code
)
test_code = clean_code(test_match.group(1))

# ---------------------------------------------------------
# Validation
# ---------------------------------------------------------

print("\nRunning AI Validation...\n")

# Page class validation

# Page class validation

page_classes = re.findall(

    r"class\s+(\w+)\s*[:\(]",

    page_code

)

if not page_classes:

    raise Exception(

        "No page classes were generated."

    )

# Prevent generic class names

invalid_classes = [

    "class BasePage",

    "class HomePage",

    "class Page"

]

for invalid in invalid_classes:

    if invalid in page_code:

        raise Exception(

            f"Invalid page class detected : {invalid}"

        )

# ---------------------------------------------
# Validate imported page classes
# ---------------------------------------------

import_match = re.search(

    rf"from\s+framework\.pages\.{page_file_name}\s+import\s+(.+)",

    step_code

)
print("\nExpected page module:", page_file_name)
print("\nGenerated step code:\n")
print(step_code)

if not import_match:

    raise Exception(

        "Step file imports incorrect page module."

    )

imported_classes = [

    cls.strip()

    for cls in import_match.group(1).split(",")

]

for cls in imported_classes:

    if f"class {cls}" not in page_code:

        raise Exception(

            f"Imported class '{cls}' not found in page object."

        )

# Prevent duplicate common step

if '@given("the demoqa website is open")' in step_code:

    # raise Exception(

    #     "Duplicate common step generated."

    # )
    pass

print("Validation Passed.")

# ---------------------------------------------------------
# Save Files
# ---------------------------------------------------------

page_file = (

    pages_dir

    / f"{base_name}_page.py"

)

step_file = (

    steps_dir

    / f"{base_name}_steps.py"

)

test_file = (

    tests_dir

    / f"test_{base_name}.py"

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

print("\n========================================")
print(" Files Generated Successfully")
print("========================================\n")

print(page_file)
print(step_file)
print(test_file)