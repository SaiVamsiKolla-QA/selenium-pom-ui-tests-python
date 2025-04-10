import tempfile
import shutil
import random
import time
import allure
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from Pages.login_page import LoginPage
from Pages.products_page import ProductPage
from Utility.utility import Utility


@pytest.fixture()
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
    driver.close()
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
@allure.feature("Product Management")
@allure.story("Add any two products")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("username,password", [
    # Test data: Standard user credentials expected to log in successfully
    pytest.param("standard_user", "secret_sauce", id="standard_user"),
])
@allure.feature('Swag Login Feature')
def test_swag_login(driver, username, password):
    """Test login functionality and verify the product page."""
    allure.dynamic.story(f"User {username} logs in")
    allure.dynamic.severity(
        allure.severity_level.CRITICAL if username == "standard_user" else allure.severity_level.NORMAL)
    allure.dynamic.description(f"Testing login with user: {username} and validating product page access")

    login_page = LoginPage(driver)
    product_page = ProductPage(driver)

    # -------------------------------
    # Step 1: Perform Login using provided credentials.
    # -------------------------------
    with allure.step(f"Login as {username}"):
        allure.attach(f"Username: {username}\nPassword: {password}",
                      name="Login Credentials",
                      attachment_type=allure.attachment_type.TEXT)

        login_page.login_as(username, password, url="https://www.saucedemo.com/")

        assert product_page.is_product_page_loaded(), f"Login failed for {username}"
        print(f"\nStep_01_Login_Successful_{username}")

        screenshot = Utility.capture_screenshot(driver, f"Step_01_Login_Successful_{username}")
        allure.attach(screenshot,
                      name="Login Successful",
                      attachment_type=allure.attachment_type.PNG)

    # -------------------------------
    # Step 2: Add two random products to the cart
    # -------------------------------
    with allure.step("Select random products to add to cart"):
        all_products = product_page.available_products.copy()
        products_to_add = random.sample(all_products, 2)
        expected_count = len(products_to_add)

        allure.attach(f"Selected products: {', '.join(products_to_add)}",
                      name="Selected Products",
                      attachment_type=allure.attachment_type.TEXT)

        print(f"\nRandomly selected products to add: {products_to_add}")

    successful_adds = 0
    # Use enumerate to create an index for each product
    for index, product_id in enumerate(products_to_add, 1):
        with allure.step(f"Add product {index}: {product_id}"):
            if product_page.add_product_to_cart(product_id):
                successful_adds += 1
                ordinal = get_ordinal(index)
                product_info = f"Added the {ordinal} Item: {product_id}"
                print(product_info)
                allure.attach(screenshot,
                              name=f"Product Added: {product_id}",
                              attachment_type=allure.attachment_type.PNG)
                allure.attach(product_info,
                              name=f"Product {index} Details",
                              attachment_type=allure.attachment_type.TEXT)

    # -------------------------------
    # Step 2.2: Verify the cart count matches the number of added products
    # -------------------------------
    with allure.step("Verify cart count"):
        time.sleep(1)
        driver.refresh()
        Utility.wait_for_page_load(driver)
        cart_count = product_page.get_cart_count()
        verification_info = f"Cart count: {cart_count}, Expected: {expected_count}"
        allure.attach(verification_info,
                      name="Cart Count Verification",
                      attachment_type=allure.attachment_type.TEXT)

        print(f"Step_02_Products_Added_{cart_count}_Items_To_Cart")
        screenshot = Utility.capture_screenshot(driver, f"Step_02_Products_Added_{cart_count}_Items_To_Cart")
        allure.attach(screenshot,
                      name="Products Added To Cart",
                      attachment_type=allure.attachment_type.PNG)

        assert cart_count == expected_count, f"Expected cart count to be {expected_count}, but got {cart_count}"
