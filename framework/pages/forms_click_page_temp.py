# framework/pages/base_page.py
from framework.utils.driver_factory import DriverFactory
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from framework.utils.logger import get_logger

logger = get_logger(__name__)

class BasePage:
    def __init__(self):
        self.driver = DriverFactory.get_driver()

    def navigate_to_forms_section(self):
        logger.info("Navigating to forms section")
        forms_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.card.upgrade-card:nth-child(1) > div.card-body > h5")))
        forms_link.click()

    def navigate_to_interactions_section(self):
        logger.info("Navigating to interactions section")
        interactions_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='element-list']//li[@id='Interactions']")))
        interactions_link.click()

    def navigate_to_resizable_option(self):
        logger.info("Navigating to resizable option")
        resizable_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='element-list']//li[@id='Resizable']")))
        resizable_link.click()

    def interact_with_resizable_box_with_restriction(self):
        logger.info("Interacting with resizable box with restriction")
        resizable_box = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#resizableBoxWithRestriction")))
        resizable_box.click()