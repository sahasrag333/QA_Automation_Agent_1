from framework.utils.driver_factory import DriverFactory
from framework.config.config import BASE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from framework.utils.logger import get_logger

logger = get_logger(__name__)

class BasePage:
    def __init__(self):
        self.driver = DriverFactory.get_driver()

    def navigate_to_homepage(self):
        self.driver.get(BASE_URL)
        logger.info("Navigated to homepage")

    def navigate_to_widgets_page(self):
        widgets_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//h5[text()='Widgets']"))
        )
        widgets_link.click()
        logger.info("Navigated to widgets page")

    def navigate_to_accordian_page(self):
        accordian_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//h5[text()='Accordian']"))
        )
        accordian_link.click()
        logger.info("Navigated to accordian page")

    def expand_accordian_section(self, section_name):
        section_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[@class='accordion']//button[text()='{section_name}']"))
        )
        section_button.click()
        logger.info(f"Expanded {section_name} section")

    def navigate_to_interactions_page(self):
        interactions_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//h5[text()='Interactions']"))
        )
        interactions_link.click()
        logger.info("Navigated to interactions page")

    def verify_interactions_page(self):
        interactions_header = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[text()='Interactions']"))
        )
        if interactions_header:
            logger.info("Interactions page displayed")
            return True
        else:
            logger.error("Interactions page not displayed")
            return False