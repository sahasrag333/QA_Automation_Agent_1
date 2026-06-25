import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://demoqa.com/")
    page.get_by_role("link", name="Widgets").click()
    page.get_by_role("link", name="Accordian").click()
    page.get_by_role("button", name="Where does it come from?").click()
    page.get_by_role("button", name="Why do we use it?").click()
    page.get_by_text("Interactions").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
