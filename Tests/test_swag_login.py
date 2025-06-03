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
@allure.feature("Authentication")
@allure.story("User Login")
def test_swag_login(driver, username, password, base_url, allure_browser_param_fixture):
    """
    Test login functionality for different user types and verify the product page.
    
    This test verifies:
    1. Login attempt with different user credentials
    2. Expected behavior for locked out users
    3. Successful navigation to product page for valid users
    """
    allure.dynamic.title(f"Login Test - {username}")
    allure.dynamic.description(f"Testing login functionality for user: {username}")
    
    login_page = LoginPage(driver)
    product_page = ProductPage(driver)

    with allure.step(f"Navigate to login page"):
        allure.attach(
            base_url,
            name="Login URL",
            attachment_type=allure.attachment_type.TEXT
        )
        login_page.open_url(base_url)

    with allure.step(f"Enter username: {username}"):
        login_page.enter_username(username)
        allure.attach(
            "Username entered successfully",
            name="Username Input",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Enter password"):
        login_page.enter_password(password)
        allure.attach(
            "Password entered successfully",
            name="Password Input",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Click login button"):
        login_page.click_login()

    # Capture post-login screenshot
    screenshot = Utility.capture_screenshot(driver, f"Login_Result_{username}")
    if screenshot:
        allure.attach(
            screenshot,
            name=f"Login_Result_{username}",
            attachment_type=allure.attachment_type.PNG
        )

    with allure.step("Verify login outcome"):
        is_product_page_loaded = product_page.is_product_page_loaded()
        
        if username == "locked_out_user":
            allure.step("Verify locked out user cannot login")
            assert not is_product_page_loaded, f"Login should have failed for {username}"
            allure.attach(
                "Login failed as expected for locked out user",
                name="Login Verification",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            allure.step("Verify successful login")
            assert is_product_page_loaded, f"Login failed for {username}"
            allure.attach(
                "Login successful - Product page loaded",
                name="Login Verification",
                attachment_type=allure.attachment_type.TEXT
            )