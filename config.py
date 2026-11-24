"""Central configuration shared by pages, fixtures and tests."""
import os
from pathlib import Path

import pytest

ROOT = Path(__file__).parent

# To try amazon.in instead:  set AMAZON_URL=https://www.amazon.in
BASE_URL = os.getenv("AMAZON_URL", "https://www.amazon.com")

# amazon.com hides "Add to Cart" when the delivery location is outside the US,
# so a US ZIP is set first.
US_ZIP = "10004"
SEARCH_TERM = "wireless mouse"

SCREENSHOT_DIR = ROOT / "screenshots"
SCREENSHOT_DIR.mkdir(exist_ok=True)

AUTH_FILE = ROOT / "auth.json"
# True when save_login.py was run: tests then use a logged-in account, so tests
# that assume a guest / empty cart are skipped. Set GUEST=1 to ignore auth.json.
LOGGED_IN = AUTH_FILE.exists() and not os.getenv("GUEST")

skip_if_logged_in = pytest.mark.skipif(
    LOGGED_IN, reason="Logged-in session: test needs a guest/empty cart"
)
