import allure
import pytest

from Pages.inventory_page import ProductPage
from Pages.login_page import LoginPage
from Utility.utility import Utility


@pytest.mark.parametrize("username,password", [
    ("standard_user", "secret_sauce"),
    ("locked_out_user", "secret_sauce"),
    ("problem_user", "secret_sauce"),
    ("performance_glitch_user", "secret_sauce"),
    ("error_user", "secret_sauce"),
    ("visual_user", "secret_sauce"),
])
@allure.epic("Swag Labs E-commerce")
@allure.feature("Swag Login Feature")
def test_swag_login(driver, username, password, base_url):
    """Test login functionality and verify the product page with screenshot attachments."""
    allure.dynamic.story(f"User {username} logs in")
    login_page = LoginPage(driver)
    product_page = ProductPage(driver)

    # Step 1: Perform login
    with allure.step(f"Login as {username}"):
        login_page.login_as(username, password, url=base_url)

    # Step 2: Verify login and capture screenshot regardless of user type
    with allure.step("Verify login outcome and attach screenshot"):
        is_product_page_loaded = product_page.is_product_page_loaded()
        screenshot_name = f"Step_01_Login_{username}"

        # Always capture a screenshot.
        screenshot = Utility.capture_screenshot(driver, screenshot_name)
        allure.attach(
            screenshot,
            name=screenshot_name,
            attachment_type=allure.attachment_type.PNG
        )

        if username == "locked_out_user":
            # For a locked out user, we expect the product page NOT to be loaded.
            assert not is_product_page_loaded, f"Login should have failed for {username}"
        else:
            # For other users, we expect the product page to load.
            assert is_product_page_loaded, f"Login failed for {username}"