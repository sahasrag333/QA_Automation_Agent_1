from pathlib import Path
import re
import ast
import json
class ValidationAgent:

    def extract_feature_steps(self, feature_file):

        feature_file = Path(feature_file)

        if not feature_file.exists():
            raise FileNotFoundError(feature_file)

        with open(
            feature_file,
            "r",
            encoding="utf-8"
        ) as f:

            content = f.readlines()

        steps = []

        pattern = r"^(Given|When|Then|And|But)\s+(.*)$"

        for line in content:

            line = line.strip()

            match = re.match(
                pattern,
                line
            )

            if match:

                steps.append(

                    {
                        "keyword": match.group(1),
                        "text": match.group(2)
                    }

                )

        return steps
    def extract_step_definitions(self, *step_files):

        steps = []

        pattern = r'@(given|when|then|step)\(\s*[\'"](.+?)[\'"]\s*\)'

        for step_file in step_files:

            step_file = Path(step_file)

            if not step_file.exists():
                continue

            with open(
                step_file,
                "r",
                encoding="utf-8"
            ) as f:

                content = f.read()

            matches = re.findall(
                pattern,
                content,
                re.IGNORECASE
            )

            for keyword, text in matches:

                steps.append(

                    {
                        "keyword": keyword.capitalize(),
                        "text": text.strip()
                    }

                )

        return steps
    def validate_steps(
    self,
    feature_steps,
    step_definitions
):

        feature_texts = []

        for step in feature_steps:

            feature_texts.append(
                step["text"].strip().lower()
            )

        definition_texts = []

        for step in step_definitions:

            definition_texts.append(
                step["text"].strip().lower()
            )
        missing_steps = []

        for feature_step in feature_texts:

            matched = False

            for definition in definition_texts:

                pattern = re.escape(definition)

                # Replace any Behave parameter like {section_name}, {button}, {username}
                pattern = re.sub(
                    r'\\\{[^}]+\\\}',
                    r'.+',
                    pattern
                )

                if re.fullmatch(
                    pattern,
                    feature_step
                ):

                    matched = True

                    break        

        if not matched:

            missing_steps.append(
                feature_step
            )
        

        if missing_steps:

            return {

                "status": "FAIL",

                "missing_steps": missing_steps

            }

        return {

            "status": "PASS",

            "missing_steps": []

        }
    

    def validate_page_methods(
        self,
        step_file,
        page_file
    ):

            with open(
                step_file,
                "r",
                encoding="utf-8"
            ) as f:

                step_tree = ast.parse(f.read())

            with open(
                page_file,
                "r",
                encoding="utf-8"
            ) as f:

                page_tree = ast.parse(f.read())

            called_methods = set()

            class MethodVisitor(ast.NodeVisitor):

                def visit_Call(self, node):

                    if isinstance(node.func, ast.Attribute):

                        called_methods.add(
                            node.func.attr
                        )

                    self.generic_visit(node)

            MethodVisitor().visit(step_tree)

            page_methods = set()

            for node in ast.walk(page_tree):

                if isinstance(node, ast.FunctionDef):

                    page_methods.add(node.name)

            ignore = {

                "__init__",

                "info",

                "debug",

                "warning",

                "error"

            }

            missing = []

            for method in called_methods:

                if method in ignore:

                    continue

                if method not in page_methods:

                    missing.append(method)

            if missing:

                return {

                    "status": "FAIL",

                    "missing_methods": sorted(missing)

                }

            return {

                "status": "PASS",

                "missing_methods": []

            }
    import ast


    def validate_imports(
        self,
        step_file,
        page_file
    ):

        with open(
            step_file,
            "r",
            encoding="utf-8"
        ) as f:

            step_tree = ast.parse(f.read())

        with open(
            page_file,
            "r",
            encoding="utf-8"
        ) as f:

            page_tree = ast.parse(f.read())

        imported_classes = []

        for node in ast.walk(step_tree):

            if isinstance(node, ast.ImportFrom):

                if node.module and node.module.startswith(
                    "framework.pages"
                ):

                    for alias in node.names:

                        imported_classes.append(
                            alias.name
                        )

        page_classes = []

        for node in ast.walk(page_tree):

            if isinstance(node, ast.ClassDef):

                page_classes.append(
                    node.name
                )

        missing = []

        for cls in imported_classes:

            if cls not in page_classes:

                missing.append(cls)

        if missing:

            return {

                "status": "FAIL",

                "missing_classes": missing

            }

        return {

            "status": "PASS",

            "missing_classes": []

        }
    
    def validate_duplicate_steps(
    self,
    step_definitions
):

        seen = {}

        duplicates = []

        for step in step_definitions:

            text = step["text"].strip().lower()

            if text in seen:

                duplicates.append(text)

            else:

                seen[text] = True

        duplicates = sorted(
            list(set(duplicates))
        )

        if duplicates:

            return {

                "status": "FAIL",

                "duplicate_steps": duplicates

            }

        return {

            "status": "PASS",

            "duplicate_steps": []

        }
    
    import json


    def save_validation_report(
        self,
        project_root,
        report
    ):

        output_file = (

            Path(project_root)

            / "framework"

            / "reports"

            / "validation_report.json"

        )

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(

            output_file,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(
                report,
                f,
                indent=4
            )

        print()

        print("Validation Report Saved")

        print(output_file)




if __name__ == "__main__":

    project_root = (
        Path(__file__)
        .resolve()
        .parents[2]
    )

    feature_file = (
        project_root
        / "framework"
        / "features"
        / "forms_click.feature"
    )

    agent = ValidationAgent()

    steps = agent.extract_feature_steps(
        feature_file
    )

    print()

    print("Feature Steps")

    print("-----------------------")

    for step in steps:

        print(step)
    step_file = (
    project_root
    / "framework"
    / "features"
    / "steps"
    / "forms_click_steps.py"
        )
    common_step_file = (
    project_root
    / "framework"
    / "features"
    / "steps"
    / "common_steps.py"
)
    step_defs = agent.extract_step_definitions(common_step_file,
    step_file
        )

    print("\nStep Definitions")
    print("-----------------------")

    for step in step_defs:

        print(step)
    print("\nValidation")
    print("-----------------------")

    result = agent.validate_steps(
        steps,
        step_defs
    )

    print(result)
    page_file = (
    project_root
    / "framework"
    / "pages"
    / "forms_click_page.py"
)

    method_result = agent.validate_page_methods(
        step_file,
        page_file
    )

    print()

    print("Page Method Validation")

    print("---------------------------")

    print(method_result)
    print()

    print("Import Validation")
    print("---------------------------")

    import_result = agent.validate_imports(
        step_file,
        page_file
    )

    print(import_result)


    print()

    print("Duplicate Step Validation")
    print("---------------------------")

    duplicate_result = agent.validate_duplicate_steps(
        step_defs
    )

    print(duplicate_result)


    validation_report = {

    "step_validation": result,

    "method_validation": method_result,

    "import_validation": import_result,

    "duplicate_validation": duplicate_result

}

    agent.save_validation_report(

        project_root,

        validation_report

    )