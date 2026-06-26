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

================================================

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
step_code = clean_code(step_match.group(1))
test_code = clean_code(test_match.group(1))

# ---------------------------------------------------------
# Validation
# ---------------------------------------------------------

print("\nRunning AI Validation...\n")

# Page class validation

if f"class {page_class}" not in page_code:

    raise Exception(
        f"{page_class} was not generated."
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

# Ensure import matches class

expected_import = (

    f"from framework.pages.{page_file_name} "

    f"import {page_class}"

)

if expected_import not in step_code:

    raise Exception(

        "Step definition imports incorrect page class."

    )

# Prevent duplicate common step

if '@given("the demoqa website is open")' in step_code:

    raise Exception(

        "Duplicate common step generated."

    )

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