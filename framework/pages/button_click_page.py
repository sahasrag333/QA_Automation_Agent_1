# button_click_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from framework.utils.driver_factory import DriverFactory
import logging

class ButtonClickPage:
    def __init__(self):
        self.driver = DriverFactory.get_driver()
        self.logger = logging.getLogger(__name__)

    def click_elements_link(self):
        elements_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//h5[text()='Elements']"))
        )
        elements_link.click()
        self.logger.info("Clicked on Elements link")

    def select_buttons_option(self):
        buttons_option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Buttons']"))
        )
        buttons_option.click()
        self.logger.info("Selected Buttons option")

    def click_click_me_button(self):
        click_me_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Click Me']"))
        )
        click_me_button.click()
        self.logger.info("Clicked on Click Me button")


###