from pathlib import Path

class FrameworkManager:

    def __init__(self, project_root):

        self.project_root = Path(project_root)

        self.framework_dir = (
            self.project_root /
            "framework"
        )

        self.required_dirs = [
            "config",
            "utils",
            "features",
            "pages",
            "step_definitions",
            "tests",
            "reports",
            "screenshots",
            "logs",
            "test_data"
        ]

    def create_structure(self):

        print("\nCreating framework structure...\n")

        for directory in self.required_dirs:

            path = self.framework_dir / directory

            path.mkdir(
                parents=True,
                exist_ok=True
            )

            print(f"✓ {path}")

        print("\nFramework structure ready.\n")

if __name__ == "__main__":
        project_root = (
            Path(__file__)
            .resolve()
            .parents[2]
        )

manager = FrameworkManager(
        project_root
    )

manager.create_structure()

