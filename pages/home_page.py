from playwright.sync_api import Page, expect

from config import BASE_URL, US_ZIP
from pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # locators
        self.search_box = page.locator("#twotabsearchtextbox")
        self.search_button = page.locator("#nav-search-submit-button")
        self.location_link = page.locator("#nav-global-location-popover-link")
        self.location_line = page.locator("#glow-ingress-line2")
        self.zip_input = page.locator("#GLUXZipUpdateInput")
        self.zip_apply = page.locator("#GLUXZipUpdate")
        self.zip_done = page.locator("button[name='glowDoneButton']").or_(
            page.get_by_role("button", name="Continue")
        )

    # ---- actions ----
    def open(self) -> None:
        """Open Amazon home page and dismiss popups."""
        self.page.set_default_timeout(20_000)
        self.goto(BASE_URL)
        self.dismiss_popups()
        self.set_us_delivery_location()

    def set_us_delivery_location(self) -> None:
        if "amazon.com" not in BASE_URL:
            return

        if self.location_line.is_visible():
            if US_ZIP in self.location_line.inner_text():
                return  # already set
        self.location_link.click()
        expect(self.zip_input).to_be_visible()
        self.zip_input.fill(US_ZIP)
        self.zip_apply.click()
        self.page.wait_for_timeout(1500)
        if self.zip_done.first.is_visible():
            self.zip_done.first.click()
        self.page.wait_for_load_state("domcontentloaded")
        expect(self.location_line).to_contain_text(US_ZIP, timeout=20_000)

    def search(self, term: str) -> None:
        self.search_box.fill(term)
        self.search_box.press("Enter")
        self.handle_captcha()

    def submit_empty_search(self) -> None:
        self.search_box.fill("")
        self.search_button.click()
        self.handle_captcha()
