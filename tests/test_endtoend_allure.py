import pytest
import random
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from Utility.utility import Utility
from Pages.login_page import LoginPage
from Pages.products_page import ProductPage
from Pages.cart_page import CartPage
from Pages.checkout_yourinformation_page import CheckoutInfoPage
from Pages.checkout_overview_page import CheckoutOverviewPage


@pytest.fixture()
def driver():
    """
    Initialize and configure the Chrome WebDriver.
    """
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.implicitly_wait(10)  # Implicit wait for element loading
    yield driver
    # Cleanup: Close the browser window and quit the driver
    driver.close()
    driver.quit()


def get_ordinal(n):
    """
    Convert a number to its ordinal representation (1st, 2nd, 3rd, etc.)
    """
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"


@allure.epic("Sauce Demo E-commerce")
@allure.feature("End-to-End Shopping Flow")
@allure.story("Complete Purchase Journey")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("username,password", [
    # Test data: Standard user credentials expected to log in successfully
    ("standard_user", "secret_sauce"),
])
def test_swag_info(driver, username, password):
    login_page = LoginPage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)
    info_page = CheckoutInfoPage(driver)
    overview_page = CheckoutOverviewPage(driver)

    # -------------------------------
    # Step 1: Perform Login using provided credentials.
    # -------------------------------
    with allure.step(f"Login as {username}"):
        login_page.login_as(username, password, url="https://www.saucedemo.com/")
        assert product_page.is_page_loaded(), f"Login failed for {username}"
        allure.attach(
            driver.get_screenshot_as_png(),
            name="login_success",
            attachment_type=allure.attachment_type.PNG
        )

    # -------------------------------
    # Step 2: Add two random products to the cart
    # -------------------------------
    with allure.step("Add random products to cart"):
        all_products = product_page.available_products.copy()
        products_to_add = random.sample(all_products, 2)
        expected_count = len(products_to_add)
        allure.attach(f"Selected products: {', '.join(products_to_add)}",
                      name="products_to_add",
                      attachment_type=allure.attachment_type.TEXT)

        successful_adds = 0
        for index, product_id in enumerate(products_to_add, 1):
            with allure.step(f"Add product: {product_id}"):
                if product_page.add_product_to_cart(product_id):
                    successful_adds += 1
                    ordinal = get_ordinal(index)
                    allure.attach(f"Added {ordinal} item: {product_id}", name=f"add_product_{index}",
                                  attachment_type=allure.attachment_type.TEXT)

        cart_count = product_page.get_cart_count()
        assert cart_count == expected_count, f"Expected cart count to be {expected_count}, but got {cart_count}"
        assert successful_adds == expected_count, f"Expected to add {expected_count} products, but added {successful_adds}"
        allure.attach(
            driver.get_screenshot_as_png(),
            name="products_added_to_cart",
            attachment_type=allure.attachment_type.PNG
        )

    # -------------------------------
    # Step 3: Navigate to the cart page.
    # -------------------------------
    with allure.step("Navigate to cart page"):
        product_page.go_to_cart()
        assert cart_page.is_cart_page_displayed(), "Failed to navigate to cart page"
        allure.attach(
            driver.get_screenshot_as_png(),
            name="cart_page",
            attachment_type=allure.attachment_type.PNG
        )

    # -------------------------------
    # Step 4: Click the checkout button.
    # -------------------------------
    with allure.step("Click checkout button"):
        checkout_success = cart_page.click_checkout()
        assert info_page.is_info_page_displayed(), "Failed to navigate to checkout info page"
        allure.attach(
            driver.get_screenshot_as_png(),
            name="checkout_info_page",
            attachment_type=allure.attachment_type.PNG
        )

    # -------------------------------
    # Step 5: Fill out the checkout information
    # -------------------------------
    with allure.step("Enter checkout information"):
        assert info_page.enter_first_name("Vamsi"), "Failed to enter first name"
        assert info_page.enter_last_name("Kolla"), "Failed to enter last name"
        assert info_page.enter_postal_code(""), "Failed to enter postal code"
        allure.attach(
            driver.get_screenshot_as_png(),
            name="checkout_info_entered",
            attachment_type=allure.attachment_type.PNG
        )

    # -------------------------------
    # Step 6: Click the continue button and verify navigation to overview page
    # -------------------------------
    with allure.step("Navigate to checkout overview"):
        info_page.click_continue()
        allure.attach(
            driver.get_screenshot_as_png(),
            name="checkout_overview_page",
            attachment_type=allure.attachment_type.PNG
        )

    # -------------------------------
    # Step 7: Complete checkout process
    # -------------------------------
    with allure.step("Complete checkout"):
        overview_page.click_finish()
        allure.attach(
            driver.get_screenshot_as_png(),
            name="checkout_complete",
            attachment_type=allure.attachment_type.PNG
        )