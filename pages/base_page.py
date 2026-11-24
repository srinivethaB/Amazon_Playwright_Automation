import re

import pytest
from playwright.sync_api import Page

from config import SCREENSHOT_DIR

ROBOT_CHECK_TEXT = re.compile(
    r"Enter the characters you see below|Type the characters you see|"
    r"Click the button below to continue shopping|verify you.?re (a )?human|"
    r"not a robot",
    re.I,
)


class BasePage:
    """Helpers shared by every page object."""

    def __init__(self, page: Page):
        self.page = page

    # ---- navigation ----
    def goto(self, url: str):
        self.page.goto(url)
        self.handle_captcha()

    # ---- screenshots ----
    def shot(self, name: str) -> None:
        self.page.screenshot(path=str(SCREENSHOT_DIR / f"{name}.png"))

    # ---- robot check ----
    def is_robot_check(self) -> bool:
        return (
            self.page.locator("input#captchacharacters").count() > 0
            or self.page.get_by_text(ROBOT_CHECK_TEXT).count() > 0
        )

    def handle_captcha(self, timeout_s: int = 180) -> None:
        """Does NOT bypass the robot check: pauses so you can solve it by hand,
        then continues automatically (waits up to 3 minutes)."""
        if not self.is_robot_check():
            return
        print("\n[!] Amazon robot check detected - solve it in the browser window...")
        self.shot("captcha_detected")
        button = self.page.get_by_role("button", name=re.compile("Continue shopping", re.I))
        if button.count() > 0:
            button.first.click()
            self.page.wait_for_load_state("domcontentloaded")
        for _ in range(timeout_s):
            if not self.is_robot_check():
                self.page.wait_for_load_state("domcontentloaded")
                return
            self.page.wait_for_timeout(1000)
        pytest.fail(f"Robot check was not solved within {timeout_s} seconds")

    # ---- popups ----
    def dismiss_popups(self) -> None:
        for selector in (
            "#sp-cc-accept",
            'button:has-text("Continue shopping")',
            'button:has-text("Dismiss")',
        ):
            popup = self.page.locator(selector).first
            if popup.is_visible():
                popup.click()
