from framework.utils.driver_factory import DriverFactory
from framework.config.config import BASE_URL
from framework.utils.logger import get_logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = get_logger(__name__)

class DemoQAHomePage:
    def __init__(self):
        self.driver = DriverFactory.get_driver()
        self.driver.get(BASE_URL)

    def navigate_to_forms_section(self):
        logger.info("Navigating to Forms section")
        forms_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.card-body > h5:nth-child(1)"))
        )
        forms_link.click()

    def navigate_to_interactions_option(self):
        logger.info("Navigating to Interactions option")
        interactions_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='element-list']//li[@id='item-0']"))
        )
        interactions_link.click()

    def navigate_to_resizable_option(self):
        logger.info("Navigating to Resizable option")
        resizable_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='element-list']//li[@id='item-1']"))
        )
        resizable_link.click()

    def is_resizable_box_with_restriction_displayed(self):
        logger.info("Checking if resizable box with restriction is displayed")
        resizable_box = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "resizableBoxWithRestriction"))
        )
        return resizable_box.is_displayed()

    def interact_with_resizable_box(self):
        logger.info("Interacting with resizable box")
        resizable_box = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "resizableBoxWithRestriction"))
        )
        resizable_box.click()