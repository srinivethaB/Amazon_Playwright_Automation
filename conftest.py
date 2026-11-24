import pytest

from config import AUTH_FILE, LOGGED_IN
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.search_results_page import SearchResultsPage


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Normal desktop viewport + US English. If auth.json exists (created by
    save_login.py) the tests run as that logged-in user. Set GUEST=1 to ignore it."""
    args = {
        **browser_context_args,
        "viewport": {"width": 1366, "height": 768},
        "locale": "en-US",
    }
    if LOGGED_IN:
        args["storage_state"] = str(AUTH_FILE)
    return args


# ---- page object fixtures ----
@pytest.fixture
def home_page(page):
    return HomePage(page)


@pytest.fixture
def results_page(page):
    return SearchResultsPage(page)


@pytest.fixture
def product_page(page):
    return ProductPage(page)


@pytest.fixture
def cart_page(page):
    return CartPage(page)


@pytest.fixture
def checkout_page(page):
    return CheckoutPage(page)


@pytest.fixture
def add_item_to_cart(home_page, results_page, product_page):
    """Reusable flow: open home -> search -> first result -> (qty) -> add to cart.
    Returns the product title."""
    from playwright.sync_api import expect
    from config import SEARCH_TERM

    def _add(term: str = SEARCH_TERM, quantity: str = None) -> str:
        home_page.open()
        home_page.search(term)
        results_page.open_first_result()
        title = product_page.get_title()
        if quantity:
            product_page.set_quantity(quantity)
        product_page.add_to_cart()
        expect(product_page.added_message).to_be_visible()
        return title

    return _add
