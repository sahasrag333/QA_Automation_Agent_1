# steps/checkbox_click_steps.py
from behave import given, when, then
from framework.pages.checkbox_click_page import CheckboxClickPage

@when("the elements link is clicked")
def step_impl(context):
    page = CheckboxClickPage()
    page.navigate_to_checkbox_link()

@when("the check box link is clicked")
def step_impl(context):
    # This step is already covered in navigate_to_checkbox_link method
    pass

@when("the select home checkbox is clicked")
def step_impl(context):
    page = CheckboxClickPage()
    page.select_home_checkbox()

@then("the select home checkbox should be selected")
def step_impl(context):
    page = CheckboxClickPage()
    assert page.is_home_checkbox_selected()


###