import pytest
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from Utility.utility import Utility
from Pages.login_page import LoginPage
from Pages.products_page import ProductPage
from Pages.cart_page import CartPage
from Pages.checkout_yourinformation_page import CheckoutInfoPage

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


@pytest.mark.parametrize("username,password", [
    # Test data: Standard user credentials expected to log in successfully
    ("standard_user", "secret_sauce"),
])
def test_swag_login(driver, username, password):
    login_page = LoginPage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)
    info_page=CheckoutInfoPage(driver)
    # -------------------------------
    # Step 1: Perform Login using provided credentials.
    # The login_as method encapsulates:
    #   - Navigating to the Sauce Demo website
    #   - Entering the username and password
    #   - Clicking the login button
    # -------------------------------
    login_page.login_as(username, password, url="https://www.saucedemo.com/")
    # -------------------------------
    # Step 1.2: Post-Login Actions
    #   - Capture a screenshot after the login attempt.
    #   - Wait for the inventory container element to verify successful login.
    # -------------------------------

    assert product_page.is_page_loaded(), f"Login failed for {username}"
    print(f"\nStep_01_Login_Successful_{username}")
    Utility.capture_screenshot(driver, f"Step_01_Login_Successful_{username}")

    # -------------------------------
    # Step 2: Add two random products to the cart
    # -------------------------------
    all_products = product_page.available_products.copy()
    products_to_add = random.sample(all_products, 2)
    expected_count = len(products_to_add)
    print(f"\nRandomly selected products to add: {products_to_add}")
    successful_adds = 0

    # Use enumerate to create an index for each product
    for index, product_id in enumerate(products_to_add, 1):
        if product_page.add_product_to_cart(product_id):
            successful_adds += 1
            ordinal = get_ordinal(index)
            print(f"Added the {ordinal} Item: {product_id}")

    # -------------------------------
    # Step 2.2: Verify the cart count matches the number of added products
    # -------------------------------
    cart_count = product_page.get_cart_count()
    assert cart_count == expected_count, f"Expected cart count to be {expected_count}, but got {cart_count}"
    assert successful_adds == expected_count, f"Expected to add {expected_count} products, but added {successful_adds}"
    print(f"Step_02_Products_Added_{cart_count}_Items_To_Cart")
    Utility.capture_screenshot(driver, f"Step_02_Products_Added_{cart_count}_Items_To_Cart")

    # -------------------------------
    # Step 3: Navigate to the cart page.
    # -------------------------------
    product_page.go_to_cart()  # This method clicks the cart icon.

    # Assert that we successfully navigated to the cart page
    assert cart_page.is_cart_page_displayed(), "Failed to navigate to cart page"
    print("\nStep_03_Cart_Items_Available_In_Cart")
    Utility.capture_screenshot(driver, "Step_03_Cart_Items are available in the cart")
    # -------------------------------
    # Step 3.2: Click the checkout button.
    # -------------------------------
    checkout_success = cart_page.click_checkout()
    assert info_page.is_info_page_displayed(), "Failed to navigate to cart page"
    print("Step_04_Cart_Page_Checkout_Clicked.")
    Utility.capture_screenshot(driver, "Step_04_Cart_Checkout_Button is Clicked..")