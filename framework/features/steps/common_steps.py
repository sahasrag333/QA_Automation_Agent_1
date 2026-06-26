from behave import given
from framework.utils.driver_factory import DriverFactory
from framework.config.config import BASE_URL


@given("the demoqa website is open")
def step_impl(context):

    driver = DriverFactory.get_driver()

    driver.get(BASE_URL)

    context.driver = driver