import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://demoqa.com/")
    page.get_by_role("link", name="Book Store Application").click()
    page.get_by_role("link", name="Profile").click()
    page.get_by_role("link", name="Profile").click()
    page.get_by_role("link", name="Book Store", exact=True).click()
    page.get_by_role("link", name="You Don't Know JS").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
