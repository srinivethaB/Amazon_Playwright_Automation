import re

from playwright.sync_api import Page

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """A guest is sent to sign-in; a logged-in user lands on the checkout page."""

    CHECKOUT_OR_SIGNIN_URL = re.compile(r"signin|checkout|/buy|/ap/", re.I)
    SIGNIN_URL = re.compile(r"signin|/ap/", re.I)

    def __init__(self, page: Page):
        super().__init__(page)
