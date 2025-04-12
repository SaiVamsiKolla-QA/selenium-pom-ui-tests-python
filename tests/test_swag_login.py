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
@allure.feature('Swag Login Feature')
def test_swag_login(driver, username, password, base_url):
    """Test login functionality and verify the product page."""
    allure.dynamic.story(f"User {username} logs in")
    login_page = LoginPage(driver)
    product_page = ProductPage(driver)
    # -------------------------------
    # Step 1: Perform Login using provided credentials.
    # -------------------------------
    with allure.step(f"Login as {username}"):
        login_page.login_as(username, password, url=base_url)

    # -------------------------------
    # Step 2: Verify login was successful by checking product page
    # -------------------------------
    with allure.step("Verify successful login"):
        is_product_page_loaded = product_page.is_product_page_loaded()

        # Take screenshot only if login was successful (we're on the product page)
        if is_product_page_loaded:
            print(f"Step_01_{username} logged in successfully")
            screenshot_name = f"Step_01_Login_Successful_{username}"
            screenshot = Utility.capture_screenshot(driver, screenshot_name)
            allure.attach(screenshot,
                          name=screenshot_name,
                          attachment_type=allure.attachment_type.PNG)

        # Assert that login was successful
        assert is_product_page_loaded, f"Login failed for {username}"
