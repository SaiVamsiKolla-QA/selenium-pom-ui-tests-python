import tempfile
import shutil
import random

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from Pages.checkout_overview_page import CheckoutOverviewPage
from Pages.checkout_yourinformation_page import CheckoutInfoPage
from Pages.login_page import LoginPage
from Pages.products_page import ProductPage
from Pages.your_cart_page import CartPage
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
@allure.feature("Checkout Process")
@pytest.mark.parametrize("username,password", [
    # Test data: Standard user credentials expected to log in successfully
    pytest.param("standard_user", "secret_sauce", id="standard_user"),
])
def test_swag_checkout_overview(driver, username, password):
    allure.dynamic.story(f"User {username} completes full checkout process")
    allure.dynamic.severity(allure.severity_level.CRITICAL)

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
        driver.refresh()
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

        screenshot = Utility.capture_screenshot(driver, "Step_03_Cart_Items are available in the cart")
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

        screenshot = Utility.capture_screenshot(driver, "Step_04_Cart_Checkout_Button is Clicked.")
        allure.attach(screenshot,
                      name="Step_04_Cart_Checkout_Button_Clicked",
                      attachment_type=allure.attachment_type.PNG)

    # -------------------------------
    # Step 5: Fill out the checkout information
    # -------------------------------
    with allure.step("Enter checkout information"):
        print("Entering checkout information")

        # Use the page object methods to enter data
        with allure.step("Enter first name: Vamsi"):
            info_page.enter_first_name("Vamsi")

        with allure.step("Enter last name: Kolla"):
            info_page.enter_last_name("Kolla")

        with allure.step("Enter postal code: T6H5J3"):
            info_page.enter_postal_code("T6H5J3")

        # Verify that the fields contain the expected values with a single method call
        with allure.step("Verify entered information"):
            info_page.verify_checkout_information("Vamsi", "Kolla", "T6H5J3")
            allure.attach("First Name: Vamsi\nLast Name: Kolla\nPostal Code: T6H5J3",
                          name="Checkout Information",
                          attachment_type=allure.attachment_type.TEXT)

        print("Step_05_Checkout_Info_Entered")
        screenshot = Utility.capture_screenshot(driver, "Step_05_Checkout_Info_Entered")
        allure.attach(screenshot,
                      name="Step_05_Checkout_Info_Entered",
                      attachment_type=allure.attachment_type.PNG)

    # -------------------------------
    # Step 6: Click the continue button and verify navigation to overview page
    # -------------------------------
    with allure.step("Click continue button and navigate to overview page"):
        print("\nStep_06_Clicking_Continue_Button")
        info_page.click_continue()
        assert overview_page.is_overview_page_loaded(), "Failed to navigate to overview page"
        print("Step_06_Checkout_Overview_Page_Displayed")

        screenshot = Utility.capture_screenshot(driver, "Step_06_Checkout_Overview_Page_Displayed")
        allure.attach(screenshot,
                      name="Step_06_Checkout_Overview_Page_Displayed",
                      attachment_type=allure.attachment_type.PNG)

    # -------------------------------
    # Step 7: Click the finish button and complete checkout
    # -------------------------------
    with allure.step("Complete checkout by clicking finish"):
        print("\nStep_07_Checkout_Complete")
        overview_page.click_finish()

        screenshot = Utility.capture_screenshot(driver, "Step_07_Checkout_Complete")
        allure.attach(screenshot,
                      name="Step_07_Checkout_Complete",
                      attachment_type=allure.attachment_type.PNG)

        allure.attach("Checkout process completed successfully",
                      name="Checkout Completion",
                      attachment_type=allure.attachment_type.TEXT)
