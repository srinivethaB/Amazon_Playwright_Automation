import pytest
from playwright.sync_api import Page

from pages.base_page import BasePage


class ProductPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.title = page.locator("#productTitle")
        self.quantity_select = page.locator("#quantity")
        self.add_to_cart_button = page.locator("#add-to-cart-button")
        self.added_message = page.locator("#NATC_SMART_WAGON_CONF_MSG_SUCCESS").or_(
            page.get_by_text("Added to cart")
        ).first

    def get_title(self) -> str:
        return self.title.inner_text().strip()

    def set_quantity(self, quantity: str) -> None:
        if self.quantity_select.count() == 0:
            pytest.skip("This product has no quantity selector")
        self.quantity_select.select_option(quantity)

    def add_to_cart(self) -> None:
        self.add_to_cart_button.click()
