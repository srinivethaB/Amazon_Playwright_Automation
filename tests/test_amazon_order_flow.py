"""
Amazon order flow (up to checkout) - Playwright + Python, Page Object Model.

Run:  pytest --headed
      pytest -m happy_path | negative | edge
"""
import re

import pytest
from playwright.sync_api import Page, expect

from config import SEARCH_TERM, skip_if_logged_in
from pages.checkout_page import CheckoutPage


# ------------------------------- HAPPY PATH ----------------------------------
@pytest.mark.happy_path
def test_amazon_order_flow_until_checkout(
    page: Page, home_page, results_page, product_page, cart_page
) -> None:
    # Step 1 - Open the home page
    home_page.open()

    expect(page).to_have_title(re.compile("Amazon", re.I))
    expect(home_page.search_box).to_be_visible()
    home_page.shot("01_home_page")

    # Step 2 - Search for a product
    home_page.search(SEARCH_TERM)
    expect(page).to_have_url(re.compile(r"[?&]k=wireless", re.I))
    expect(results_page.results.first).to_be_visible()
    assert results_page.results.count() > 0, "Search returned no results"
    home_page.shot("02_search_results")

    # Step 3 - Select the first product
    results_page.open_first_result()
    expect(product_page.title).to_be_visible()
    product_title = product_page.get_title()
    print(f"\nSelected product: {product_title}")
    product_page.shot("03_product_page")

    # Step 4 - Add to cart
    expect(product_page.add_to_cart_button).to_be_visible()
    product_page.add_to_cart()
    expect(product_page.added_message).to_be_visible()
    product_page.shot("04_added_to_cart")

    # Step 5 - Verify the cart
    cart_page.open()
    cart_page.shot("05_cart_page")
    expect(cart_page.item_title(product_title)).to_be_visible()
    expect(cart_page.subtotal(1)).to_be_visible()

    # Step 6 - Proceed to checkout, then STOP (no order is placed)
    cart_page.proceed_to_checkout()
    expect(page).to_have_url(CheckoutPage.CHECKOUT_OR_SIGNIN_URL)
    cart_page.shot("06_checkout_reached")
    print("Reached checkout. Stopping here - no order placed.")


# ------------------------------ NEGATIVE tests --------------------------------
@pytest.mark.negative
def test_search_with_no_matching_results(home_page, results_page) -> None:
    """Gibberish search should show a 'No results' message, not break the page."""
    home_page.open()
    home_page.search("asdfqwerzxcv123zzxx")
    expect(results_page.no_results_message).to_be_visible()
    home_page.shot("neg_01_no_results")


@pytest.mark.negative
def test_empty_search_does_not_break_page(page: Page, home_page) -> None:
    home_page.open()
    home_page.submit_empty_search()
    expect(page).to_have_url(re.compile(r"amazon\.(com|in)"))
    expect(home_page.search_box).to_be_visible()
    home_page.shot("neg_02_empty_search")


@pytest.mark.negative
@skip_if_logged_in
def test_new_session_cart_is_empty(home_page, cart_page) -> None:
    """A fresh guest session should show an empty cart and no checkout button."""
    home_page.open()
    cart_page.open()
    expect(cart_page.empty_message).to_be_visible()
    expect(cart_page.checkout_button).to_have_count(0)
    cart_page.shot("neg_03_empty_cart")


@pytest.mark.negative
@skip_if_logged_in
def test_guest_checkout_requires_sign_in(page: Page, add_item_to_cart, cart_page) -> None:
    """A guest must not reach the payment step without signing in."""
    add_item_to_cart()
    cart_page.open()
    cart_page.proceed_to_checkout()
    expect(page).to_have_url(CheckoutPage.SIGNIN_URL)
    cart_page.shot("neg_04_guest_checkout_signin")


# -------------------------------- EDGE tests ----------------------------------
@pytest.mark.edge
@skip_if_logged_in
def test_remove_item_empties_cart(add_item_to_cart, cart_page) -> None:
    """Deleting the only item should show the 'removed' or 'empty' message."""
    add_item_to_cart()
    cart_page.open()
    cart_page.delete_first_item()
    expect(cart_page.removed_or_empty_message).to_be_visible()
    cart_page.shot("edge_02_item_removed")



@pytest.mark.edge
@pytest.mark.parametrize(
    "term",
    ["!@#$%^&*()<>", "a" * 300],
    ids=["special_characters", "very_long_text"],
)
def test_search_special_and_long_input(page: Page, home_page, term: str) -> None:
    home_page.open()
    home_page.search(term)
    expect(page).to_have_url(re.compile(r"amazon\.(com|in)"))
    expect(home_page.search_box).to_be_visible()
    home_page.shot(f"edge_03_input_{len(term)}_chars")
