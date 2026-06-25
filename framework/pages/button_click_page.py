from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from framework.utils.driver_factory import DriverFactory
from framework.config.config import BASE_URL
from framework.utils.logger import get_logger

class HomePage:
    def __init__(self):
        self.driver = DriverFactory.get_driver()
        self.logger = get_logger(__name__)

    def open(self):
        self.driver.get(BASE_URL)
        self.logger.info("Opening application")

    def click_elements_link(self):
        elements_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//h5[text()='Elements']"))
        )
        elements_link.click()
        self.logger.info("Clicked on Elements link")

    def click_buttons_option(self):
        buttons_option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Buttons']"))
        )
        buttons_option.click()
        self.logger.info("Clicked on Buttons option")

class ButtonsPage:
    
    
    def __init__(self):
        self.driver = DriverFactory.get_driver()
        self.logger = get_logger(__name__)
        
    def click_click_me_button(self):
        click_me_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Click Me']"))
        )
        click_me_button.click()
        self.logger.info("Clicked on Click Me button")

    def is_click_me_button_clicked(self):

        message = WebDriverWait(
            self.driver,
            10
        ).until(
            EC.visibility_of_element_located(
                (By.ID, "dynamicClickMessage")
            )
        )

        return (
            "You have done a dynamic click"
            in message.text
        )