# checkbox_click_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from framework.utils.driver_factory import DriverFactory
import logging

class CheckboxClickPage:
    def __init__(self):
        self.driver = DriverFactory.get_driver()
        self.BASE_URL = "https://demoqa.com/"
        self.logger = logging.getLogger(__name__)

    def navigate_to_checkbox_link(self):
        self.driver.get(self.BASE_URL)
        elements_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//h5[text()='Elements']"))
        )
        elements_link.click()
        checkbox_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Check Box']"))
        )
        checkbox_link.click()

    def select_home_checkbox(self):
        home_checkbox = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@class='rct-checkbox']//input[@type='checkbox']"))
        )
        home_checkbox.click()

    def is_home_checkbox_selected(self):
        home_checkbox = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='rct-checkbox']//input[@type='checkbox']"))
        )
        return home_checkbox.is_selected()


###