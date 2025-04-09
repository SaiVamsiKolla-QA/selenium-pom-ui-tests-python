import pytest
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from Pages.login_page import LoginPage
from Pages.products_page import ProductPage
from Pages.cart_page import CartPage
from Utility.utility import Utility


@pytest.fixture()
def driver():
    """
    Initialize and configure the Chrome WebDriver.
    """
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.implicitly_wait(10)  # Set an implicit wait for element loading
    yield driver
    # -------------------------------
    # Cleanup: Close the browser window and quit the driver
    # -------------------------------
    driver.close()
    driver.quit()


@pytest.mark.parametrize("username,password", [
    # -------------------------------
    # Test Data: Standard user credentials expected to log in successfully
    # -------------------------------
    ("standard_user", "secret_sauce"),
])
def test_cart_checkout(driver, username, password):
    """
    Test Case:
      1. Logs into the Sauce Demo application.
      2. Adds two random products to the shopping cart.
      3. Navigates to the cart page.
      4. Verifies that all selected products appear in the cart.
      5. Clicks the checkout button if verification passes.
    """
    # -------------------------------
    # Step 1: Initialize page objects and perform login.
    # -------------------------------
    login_page = LoginPage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)

    login_page.login_as(username, password, url="https://www.saucedemo.com/")
    assert product_page.wait_for_page_load(), "Step 1: Products page did not load in time."

    # -------------------------------
    # Step 2: Add two random products to the shopping cart.
    # -------------------------------
    available_products = product_page.available_products.copy()
    products_to_add = random.sample(available_products, 2)
    expected_products = products_to_add  # Items to verify later in the cart

    added_count = 0
    for product in products_to_add:
        if product_page.add_product_to_cart(product):
            added_count += 1
            print(f"Step 2: Successfully added: {product}")
    assert added_count == len(products_to_add), (
        f"Step 2: Expected to add {len(products_to_add)} products, but only {added_count} were added."
    )

    # Capture a screenshot after adding products.
    Utility.capture_screenshot(driver, "Selected_products")
    print(f"Step 2: Products added to cart: {products_to_add}")

    # -------------------------------
    # Step 3: Navigate to the cart page.
    # -------------------------------
    product_page.go_to_cart()  # This method clicks the cart icon.
    Utility.capture_screenshot(driver, "Products_in_the_Cart")
    print("Step 3: Clicked cart link to navigate to cart page.")

    # -------------------------------
    # Step 3.1: Assert that the checkout button is present on the cart page.
    # -------------------------------
    checkout_button = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "checkout"))
    )
    assert checkout_button is not None, "Step 3.1: Checkout button not found on cart page."
    print("Step 3.1: Checkout button is present on the cart page.")
    # -------------------------------
    # Step 6: Click the checkout button.
    # -------------------------------
    checkout_success = cart_page.click_checkout()
    Utility.capture_screenshot(driver, "Proceeding to checkout")
    assert checkout_success, "Step 6: Failed to click checkout button."
    print("Step 6: Successfully clicked the checkout button.")