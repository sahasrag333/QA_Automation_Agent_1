from behave import given, when, then
from framework.pages.widget_click_page import BasePage

@given('I am on the DemoQA homepage')
def step_impl(context):
    base_page = BasePage()
    base_page.navigate_to_homepage()

@when('I navigate to the Widgets page')
def step_impl(context):
    base_page = BasePage()
    base_page.navigate_to_widgets_page()

@when('I click on the Accordian link')
def step_impl(context):
    base_page = BasePage()
    base_page.navigate_to_accordian_page()

@when('I expand the "{section_name}" section')
def step_impl(context, section_name):
    base_page = BasePage()
    base_page.expand_accordian_section(section_name)

@when('I click on the Interactions link')
def step_impl(context):
    base_page = BasePage()
    base_page.navigate_to_interactions_page()

@then('the Interactions page should be displayed')
def step_impl(context):
    base_page = BasePage()
    assert base_page.verify_interactions_page()