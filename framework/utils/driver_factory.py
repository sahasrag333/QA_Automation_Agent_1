from selenium import webdriver

class DriverFactory:

    _driver = None

    @classmethod
    def get_driver(cls):

        if cls._driver is None:

            options = webdriver.ChromeOptions()

            cls._driver = webdriver.Chrome(options=options)

            cls._driver.maximize_window()

        return cls._driver

    @classmethod
    def quit_driver(cls):

        if cls._driver:

            cls._driver.quit()

            cls._driver = None