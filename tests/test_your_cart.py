import tempfile
import shutil
import random

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from Pages.checkout_yourinformation_page import CheckoutInfoPage
from Pages.login_page import LoginPage
from Pages.products_page import ProductPage
from Pages.your_cart_page import CartPage
from Utility.utility import Utility


@pytest.fixture(scope='function')
def driver():
    """
    Initialize and configure the Chrome WebDriver.
    """
    # Create a unique temporary directory for Chrome's user data
    user_data_dir = tempfile.mkdtemp(prefix="chrome_userdata_")
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=chrome_options
    )
    driver.implicitly_wait(10)
    yield driver
    # Quit the driver and remove the temporary directory
    driver.quit()
    shutil.rmtree(user_data_dir, ignore_errors=True)


def get_ordinal(n):
    """
    Convert a number to its ordinal representation (1st, 2nd, 3rd, etc.)
    """
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"


@allure.epic("Swag Labs E-commerce")
@allure.feature("Shopping Cart")
@pytest.mark.parametrize("username,password", [
    # Test data: Standard user credentials expected to log in successfully
    pytest.param("standard_user", "secret_sauce", id="standard_user"),
])
def test_swag_your_cart(driver, username, password):
    allure.dynamic.story(f"User {username} adds products to cart and proceeds to checkout")
    allure.dynamic.severity(allure.severity_level.CRITICAL)

    login_page = LoginPage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)
    info_page = CheckoutInfoPage(driver)

    # -------------------------------
    # Step 1: Perform Login using provided credentials.
    # -------------------------------
    with allure.step(f"Login as {username}"):
        login_page.login_as(username, password, url="https://www.saucedemo.com/")
        assert product_page.is_product_page_loaded(), f"Login failed for {username}"
        print(f"\nStep_01_Login_Successful_{username}")
        screenshot = Utility.capture_screenshot(driver, f"Step_01_Login_Successful_{username}")
        allure.attach(screenshot,
                      name=f"Step_01_Login_Successful_{username}",
                      attachment_type=allure.attachment_type.PNG)

    # -------------------------------
    # Step 2: Add two random products to the cart
    # -------------------------------
    with allure.step("Select and add random products to cart"):
        all_products = product_page.available_products.copy()
        products_to_add = random.sample(all_products, 2)
        expected_count = len(products_to_add)

        product_list = ", ".join(products_to_add)
        allure.attach(f"Products to add: {product_list}",
                      name="Selected Products",
                      attachment_type=allure.attachment_type.TEXT)

        print(f"\nRandomly selected products to add: {products_to_add}")
        successful_adds = 0

        for index, product_id in enumerate(products_to_add, 1):
            with allure.step(f"Add product {index}: {product_id}"):
                if product_page.add_product_to_cart(product_id):
                    successful_adds += 1
                    ordinal = get_ordinal(index)
                    print(f"Added the {ordinal} Item: {product_id}")

    # -------------------------------
    # Step 2.2: Verify the cart count matches the number of added products
    # -------------------------------
    with allure.step("Verify cart count"):
        cart_count = product_page.get_cart_count()
        print(f"Step_02_Products_Added_{cart_count}_Items_To_Cart")

        screenshot = Utility.capture_screenshot(driver, f"Step_02_Products_Added_{cart_count}_Items_To_Cart")
        allure.attach(screenshot,
                      name=f"Step_02_Products_Added_{cart_count}_Items_To_Cart",
                      attachment_type=allure.attachment_type.PNG)

        allure.attach(f"Cart count: {cart_count}, Expected: {expected_count}",
                      name="Cart Count Verification",
                      attachment_type=allure.attachment_type.TEXT)

        assert cart_count == expected_count, f"Expected cart count to be {expected_count}, but got {cart_count}"

    # -------------------------------
    # Step 3: Navigate to the cart page.
    # -------------------------------
    with allure.step("Navigate to cart page"):
        product_page.go_to_cart()
        # Assert that we successfully navigated to the cart page
        assert cart_page.is_cart_page_loaded(), "Failed to navigate to cart page"
        print("\nStep_03_Cart_Items_Available_In_Cart")

        screenshot = Utility.capture_screenshot(driver, "Step_03_Cart_Items_Available_In_Cart")
        allure.attach(screenshot,
                      name="Step_03_Cart_Items_Available_In_Cart",
                      attachment_type=allure.attachment_type.PNG)

    # -------------------------------
    # Step 4: Click the checkout button.
    # -------------------------------
    with allure.step("Click checkout button"):
        cart_page.click_checkout()
        assert info_page.is_info_page_loaded(), "Failed to navigate to checkout information page"
        print("Step_04_Cart_Page_Checkout_Clicked.")

        screenshot = Utility.capture_screenshot(driver, "Step_04_Cart_Checkout_Button_Clicked")
        allure.attach(screenshot,
                      name="Step_04_Cart_Checkout_Button_Clicked",
                      attachment_type=allure.attachment_type.PNG)
