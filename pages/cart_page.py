import re

from playwright.sync_api import Page

from config import BASE_URL
from pages.base_page import BasePage

# Matches: "Your Amazon Cart is empty", "your cart is empty", "Your Shopping Cart is empty"
EMPTY_CART_TEXT = re.compile(
    r"your\s+(amazon\s+|shopping\s+)?cart\s+(is|was)\s+empty", re.I
)
# Matches: "was removed from Shopping Cart", "has been deleted from your cart"
DELETED_TEXT = re.compile(
    r"(was|has\s+been|have\s+been)?\s*(removed|deleted)\s+from\s+(your\s+)?(amazon\s+|shopping\s+)?cart",
    re.I,
)


class CartPage(BasePage):
    URL = f"{BASE_URL}/gp/cart/view.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.checkout_button = page.get_by_role("button", name=re.compile(r"Proceed to checkout", re.I))
        self.delete_button = page.get_by_role("button", name=re.compile(r"^Delete", re.I)).first
        self.empty_message = page.get_by_text(EMPTY_CART_TEXT).first
        self.deleted_message = page.get_by_text(DELETED_TEXT).first
        self.removed_or_empty_message = page.get_by_text(DELETED_TEXT).or_(
            page.get_by_text(EMPTY_CART_TEXT)
        ).first

    def open(self) -> None:
        self.goto(self.URL)

    def item_title(self, title: str):
        """Cart titles are shortened, so match the first three words."""
        first_words = " ".join(title.split()[:3])
        cart_list = self.page.get_by_role("list", name="Shopping Cart")
        return cart_list.get_by_role(
            "heading", name=re.compile(re.escape(first_words), re.I)
        ).first

    def subtotal(self, items: int = 1):
        word = "item" if items == 1 else "items"
        return self.page.get_by_role(
            "heading", name=re.compile(rf"Subtotal \({items} {word}\)", re.I)
        ).first

    def proceed_to_checkout(self) -> None:
        self.checkout_button.first.click()
        self.handle_captcha()

    def delete_first_item(self) -> None:
        self.delete_button.click()
