from pathlib import Path
import json
import shutil


class HealingEngine:

    # --------------------------------------------------
    # Create Temporary Healed Page
    # --------------------------------------------------

    def apply_first_fix(
        self,
        project_root,
        feature_name
    ):

        project_root = Path(project_root)

        report_file = (
            project_root
            / "framework"
            / "reports"
            / "healing_report.json"
        )

        with open(
            report_file,
            "r",
            encoding="utf-8"
        ) as f:

            report = json.load(f)
        # ---------------------------------------
# No locator found
# ---------------------------------------

        if report.get("status") == "NO_LOCATOR_FOUND":

            print("\nNo locator found for healing.")

            return None
        
        page_file = (
            project_root
            / "framework"
            / "pages"
            / f"{feature_name}_page.py"
        )

        temp_file = (
            project_root
            / "framework"
            / "pages"
            / f"{feature_name}_page_temp.py"
        )

        shutil.copy(
            page_file,
            temp_file
        )

        original = report["original_locator"]

        replacement = report["suggestions"][0]

        with open(
            temp_file,
            "r",
            encoding="utf-8"
        ) as f:

            content = f.read()

        content = content.replace(
            original,
            replacement
        )

        with open(
            temp_file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(content)

        print("\n========== HEALING ENGINE ==========")

        print(f"Original Locator   : {original}")
        print(f"Suggested Locator  : {replacement}")
        print(f"Temporary Page     : {temp_file}")

        return temp_file

    # --------------------------------------------------
    # Backup Original Page Object
    # --------------------------------------------------

    def backup_original_page(
        self,
        page_file
    ):

        backup_file = page_file.with_name(
            page_file.stem + "_backup.py"
        )

        shutil.copy(
            page_file,
            backup_file
        )

        print(f"\nBackup Created : {backup_file}")

        return backup_file

    # --------------------------------------------------
    # Replace Original With Healed Page
    # --------------------------------------------------

    def apply_healed_page(
        self,
        temp_file,
        original_file
    ):

        shutil.copy(
            temp_file,
            original_file
        )

        print("Temporary page applied successfully.")

    # --------------------------------------------------
    # Restore Original Page
    # --------------------------------------------------

    def restore_original_page(
        self,
        backup_file,
        original_file
    ):

        shutil.copy(
            backup_file,
            original_file
        )

        backup_file.unlink(
            missing_ok=True
        )

        print("Original page restored.")

    # --------------------------------------------------
    # Cleanup Temporary Page
    # --------------------------------------------------

    def cleanup_temp_page(
        self,
        temp_file
    ):

        temp_file = Path(temp_file)

        if temp_file.exists():

            temp_file.unlink()

            print("Temporary page deleted.")


# --------------------------------------------------
# Standalone Test
# --------------------------------------------------

if __name__ == "__main__":

    project_root = (
        Path(__file__)
        .resolve()
        .parents[2]
    )

    feature_name = "widget_click"

    engine = HealingEngine()

    temp_file = engine.apply_first_fix(
        project_root,
        feature_name
    )

    original_page = (
        project_root
        / "framework"
        / "pages"
        / f"{feature_name}_page.py"
    )

    backup = engine.backup_original_page(
        original_page
    )

    engine.apply_healed_page(
        temp_file,
        original_page
    )

    engine.restore_original_page(
        backup,
        original_page
    )

    engine.cleanup_temp_page(
        temp_file
    )