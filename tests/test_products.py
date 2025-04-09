import pytest
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from Utility.utility import Utility
from Pages.login_page import LoginPage
from Pages.products_page import ProductPage


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


@pytest.mark.parametrize("username,password", [
    # Test data: Standard user credentials expected to log in successfully
    ("standard_user", "secret_sauce"),
])
def test_add_product(driver, username, password):
    """
    Test case: Add two random products to the cart.

    This test performs the following steps:
      1. Logs in to the Sauce Demo application.
      2. Waits for the products page to load.
      3. Randomly selects and adds two products to the cart.
      4. Captures a screenshot after adding the products.
      5. Verifies that the cart count matches the expected number.
    """
    # -------------------------------
    # Step 1: Initialize Page Objects and log in
    # -------------------------------
    login_page = LoginPage(driver)
    product_page = ProductPage(driver)


    # Step 1: Login into the application
    login_page.login_as(username, password, url="https://www.saucedemo.com/")

    # -------------------------------
    # Step 2: Wait for the Products page to load
    # -------------------------------
    assert product_page.wait_for_page_load(), "Products page did not load in time."

    # -------------------------------
    # Step 3: Add two random products to the cart
    # -------------------------------
    all_products = product_page.available_products.copy()
    products_to_add = random.sample(all_products, 2)
    expected_count = len(products_to_add)
    print(f"Randomly selected products to add: {products_to_add}")

    successful_adds = 0
    for product_id in products_to_add:
        if product_page.add_product_to_cart(product_id):
            successful_adds += 1
            print(f"Successfully added: {product_id}")

    # -------------------------------
    # Step 4: Capture a screenshot after adding products
    # -------------------------------
    Utility.capture_screenshot(driver, "Adding products to the cart")
    print("Screenshot captured after adding all products to cart.")

    # -------------------------------
    # Step 5: Verify the cart count matches the number of added products
    # -------------------------------
    cart_count = product_page.get_cart_count()
    assert cart_count == expected_count, f"Expected cart count to be {expected_count}, but got {cart_count}"
    assert successful_adds == expected_count, f"Expected to add {expected_count} products, but added {successful_adds}"
    print(f"Successfully added all {cart_count} products to cart.")
    print("Test passed: All products were successfully added to cart.")
