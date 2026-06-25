from pathlib import Path
import sys

project_root = Path(__file__).resolve().parent

sys.path.insert(
    0,
    str(project_root)
)

from framework.utils.driver_factory import DriverFactory
from agents.screenshot_agent.screenshot_agent import ScreenshotAgent


driver = DriverFactory.get_driver()

driver.get(
    "https://demoqa.com"
)

agent = ScreenshotAgent(
    project_root
)

agent.capture(driver)

driver.quit()