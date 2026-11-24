import re

from playwright.sync_api import Page

from pages.base_page import BasePage


class SearchResultsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.results = page.locator('div[data-component-type="s-search-result"]')
        self.first_result_link = self.results.locator("a:has(h2), h2 a").first
        self.no_results_message = page.get_by_text(re.compile(r"No results for", re.I)).first

    def open_first_result(self) -> None:
        self.first_result_link.click()
        self.handle_captcha()
