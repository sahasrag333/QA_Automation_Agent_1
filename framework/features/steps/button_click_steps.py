from behave import given, when, then
from framework.pages.button_click_page import HomePage, ButtonsPage



@when("the Elements link is clicked")
def step_impl(context):
    home_page = HomePage()
    home_page.click_elements_link()

@when("the Buttons option is selected")
def step_impl(context):
    home_page = HomePage()
    home_page.click_buttons_option()
    
@when('the Click Me button is clicked')
def step_impl(context):
    buttons_page = ButtonsPage()
    buttons_page.click_click_me_button()

@then("the Click Me button should be in a clicked state")
def step_impl(context):
    buttons_page = ButtonsPage()
    assert buttons_page.is_click_me_button_clicked()