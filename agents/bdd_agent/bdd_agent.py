from pathlib import Path
import sys

# Ensure repository root is on sys.path so imports resolve when running this file
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from agents.utils.llm import generate

recordings_dir = project_root /"framework" / "recordings"
features_dir = project_root / "framework" / "features"

features_dir.mkdir(parents=True, exist_ok=True)

# --------------------------
# Select Recording File
# --------------------------

if len(sys.argv) > 1:
    
    base_name = sys.argv[1]

    input_file = (
        recordings_dir /
        f"{base_name}.py"
    )

    if not input_file.is_absolute():
        input_file = project_root / input_file
else:
    py_files = sorted(recordings_dir.glob("*.py"))

    if not py_files:
        raise FileNotFoundError(
            f"No recording files found in {recordings_dir}"
        )

    input_file = py_files[0]

# --------------------------
# Read Recording
# --------------------------

playwright_code = input_file.read_text(
    encoding="utf-8"
)

# --------------------------
# Prompt
# --------------------------

prompt = f"""
You are a Senior QA Automation Architect.

Convert this Playwright recording into a valid BDD Gherkin feature file.

Rules:

- Generate meaningful Feature name
- Generate meaningful Scenario name
- Use Given When Then
- Use business readable language
- Do not mention Playwright
- Do not explain anything
- Do not use markdown
- Output only Gherkin

Recording:

{playwright_code}
"""

feature_content = generate(
    prompt=prompt,
    task_type="bdd"
)

feature_content = (
    feature_content
    .replace("```gherkin", "")
    .replace("```", "")
    .strip()
)

# --------------------------
# Save Feature File
# --------------------------

feature_file = (
    features_dir /
    f"{input_file.stem}.feature"
)

feature_file.write_text(
    feature_content,
    encoding="utf-8"
)

print(f"\nFeature created:\n{feature_file}")