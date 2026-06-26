from behave import given, when, then
from framework.pages.forms_click_page import DemoQAHomePage

@given("the demoqa website is open")
def step_impl(context):
    context.demoqa_home_page = DemoQAHomePage()

@when("the user navigates to the Forms section")
def step_impl(context):
    context.demoqa_home_page.navigate_to_forms_section()

@when("the user selects the Interactions option")
def step_impl(context):
    context.demoqa_home_page.navigate_to_interactions_option()

@when("the user chooses the Resizable option")
def step_impl(context):
    context.demoqa_home_page.navigate_to_resizable_option()

@then("the resizable box with restriction is displayed and can be interacted with")
def step_impl(context):
    assert context.demoqa_home_page.is_resizable_box_with_restriction_displayed()
    context.demoqa_home_page.interact_with_resizable_box()