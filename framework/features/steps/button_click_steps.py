# steps/button_click_steps.py
from behave import given, when, then
from framework.pages.button_click_page import ButtonClickPage
import logging

@when('the Elements link is clicked')
def step_impl(context):
    button_click_page = ButtonClickPage()
    button_click_page.click_elements_link()

@when('the Buttons option is selected')
def step_impl(context):
    button_click_page = ButtonClickPage()
    button_click_page.select_buttons_option()

@then('the Click Me button is clicked')
def step_impl(context):
    button_click_page = ButtonClickPage()
    button_click_page.click_click_me_button()


###