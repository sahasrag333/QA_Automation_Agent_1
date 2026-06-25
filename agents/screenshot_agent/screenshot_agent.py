from pathlib import Path
from datetime import datetime

class ScreenshotAgent:


    def __init__(self, project_root):

        self.project_root = Path(project_root)

        self.screenshot_dir = (
            self.project_root /
            "framework" /
            "screenshots"
        )

        self.screenshot_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def capture(self, driver):

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        screenshot_file = (
            self.screenshot_dir /
            f"failure_{timestamp}.png"
        )

        driver.save_screenshot(
            str(screenshot_file)
        )

        print(
            f"\nScreenshot Saved:\n{screenshot_file}"
        )

        return str(screenshot_file)

