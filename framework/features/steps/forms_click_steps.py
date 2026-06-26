# framework/step_definitions/interacting_with_resizable_box_steps.py
from behave import given, when, then
from framework.pages.forms_click_page import DemoQAHomePage
from framework.config.config import BASE_URL
from framework.utils.logger import get_logger

logger = get_logger(__name__)



@when('the user navigates to the forms section')
def step_impl(context):
    base_page = DemoQAHomePage()
    base_page.navigate_to_forms_section()

@when('the user selects the interactions option')
def step_impl(context):
    base_page = DemoQAHomePage()
    base_page.navigate_to_interactions_section()

@when('the user chooses the resizable option')
def step_impl(context):
    base_page = DemoQAHomePage()
    base_page.navigate_to_resizable_option()

@when('the user clicks on the resizable box with restriction')
def step_impl(context):
    base_page = DemoQAHomePage()
    base_page.interact_with_resizable_box_with_restriction()

@then('the resizable box with restriction is interacted with')
def step_impl(context):
    logger.info("Resizable box with restriction is interacted with")
    # Add assertion to verify interaction