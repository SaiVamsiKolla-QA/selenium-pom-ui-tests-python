import random
import shutil
import tempfile
import time
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from Pages.login_page import LoginPage
from Pages.products_page import ProductPage
from Pages.your_cart_page import CartPage
from Pages.checkout_yourinformation_page import CheckoutInfoPage
from Pages.checkout_overview_page import CheckoutOverviewPage
from Utility.utility import Utility


# Shared utility function
def get_ordinal(n):
    """Convert a number to its ordinal representation (1st, 2nd, 3rd, etc.)"""
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"


# Base driver fixture
@pytest.fixture(scope='function')
def driver():
    """Initialize and configure the Chrome WebDriver."""
    user_data_dir = tempfile.mkdtemp(prefix="chrome_userdata_")
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=chrome_options
    )
    driver.implicitly_wait(10)
    yield driver
    driver.quit()
    shutil.rmtree(user_data_dir, ignore_errors=True)


# Login fixture
@pytest.fixture
def logged_in_standard_user(driver):
    """Fixture that logs in as standard_user and returns the product page"""
    username = "standard_user"
    password = "secret_sauce"

    login_page = LoginPage(driver)
    product_page = ProductPage(driver)

    # Login step
    with allure.step(f"Login as {username}"):
        login_page.login_as(username, password, url="https://www.saucedemo.com/")

        assert product_page.is_product_page_loaded(), f"Login failed for {username}"
        print(f"\nStep_01_Login_Successful_{username}")

        screenshot = Utility.capture_screenshot(driver, f"Step_01_Login_Successful_{username}")
        allure.attach(screenshot,
                      name="Login Successful",
                      attachment_type=allure.attachment_type.PNG)

    return product_page


# Products added to cart fixture
@pytest.fixture
def products_added_to_cart(logged_in_standard_user, driver):
    """Fixture that adds 2 random products to cart and returns product page and product IDs"""
    product_page = logged_in_standard_user

    with allure.step("Select random products to add to cart"):
        all_products = product_page.available_products.copy()
        products_to_add = random.sample(all_products, 2)
        expected_count = len(products_to_add)

        product_list = ", ".join(products_to_add)
        allure.attach(f"Products to add: {product_list}",
                      name="Selected Products",
                      attachment_type=allure.attachment_type.TEXT)

        print(f"\nRandomly selected products to add: {products_to_add}")

        for index, product_id in enumerate(products_to_add, 1):
            with allure.step(f"Add product {index}: {product_id}"):
                if product_page.add_product_to_cart(product_id):
                    ordinal = get_ordinal(index)
                    print(f"Added the {ordinal} Item: {product_id}")

    # Verify cart count
    with allure.step("Verify cart count"):
        driver.refresh()
        cart_count = product_page.get_cart_count()
        print(f"Step_02_Products_Added_{cart_count}_Items_To_Cart")

        screenshot = Utility.capture_screenshot(driver, f"Step_02_Products_Added_{cart_count}_Items_To_Cart")
        allure.attach(screenshot,
                      name=f"Step_02_Products_Added_{cart_count}_Items_To_Cart",
                      attachment_type=allure.attachment_type.PNG)

        assert cart_count == expected_count, f"Expected cart count to be {expected_count}, but got {cart_count}"

    return product_page, products_to_add


# Cart page fixture
@pytest.fixture
def cart_page_loaded(products_added_to_cart, driver):
    """Fixture that navigates to cart page and returns the cart page"""
    product_page, _ = products_added_to_cart
    cart_page = CartPage(driver)

    with allure.step("Navigate to cart page"):
        product_page.go_to_cart()
        assert cart_page.is_cart_page_loaded(), "Failed to navigate to cart page"
        print("\nStep_03_Cart_Items_Available_In_Cart")

        screenshot = Utility.capture_screenshot(driver, "Step_03_Cart_Items_Available_In_Cart")
        allure.attach(screenshot,
                      name="Step_03_Cart_Items_Available_In_Cart",
                      attachment_type=allure.attachment_type.PNG)

    return cart_page


# Checkout info page fixture
@pytest.fixture
def checkout_info_page_loaded(cart_page_loaded, driver):
    """Fixture that clicks checkout and returns the info page"""
    cart_page = cart_page_loaded
    info_page = CheckoutInfoPage(driver)

    with allure.step("Click checkout button"):
        cart_page.click_checkout()
        assert info_page.is_info_page_loaded(), "Failed to navigate to checkout information page"
        print("Step_04_Cart_Page_Checkout_Clicked.")

        screenshot = Utility.capture_screenshot(driver, "Step_04_Cart_Checkout_Button_Clicked")
        allure.attach(screenshot,
                      name="Step_04_Cart_Checkout_Button_Clicked",
                      attachment_type=allure.attachment_type.PNG)

    return info_page


# Checkout info filled fixture
@pytest.fixture
def checkout_info_filled(checkout_info_page_loaded, driver):
    """Fixture that fills checkout info and returns the info page"""
    info_page = checkout_info_page_loaded

    with allure.step("Enter checkout information"):
        print("Entering checkout information")

        with allure.step("Enter first name: Vamsi"):
            info_page.enter_first_name("Vamsi")

        with allure.step("Enter last name: Kolla"):
            info_page.enter_last_name("Kolla")

        with allure.step("Enter postal code: T6H5J3"):
            info_page.enter_postal_code("T6H5J3")

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

    return info_page


# Overview page fixture
@pytest.fixture
def overview_page_loaded(checkout_info_filled, driver):
    """Fixture that navigates to overview page and returns it"""
    info_page = checkout_info_filled
    overview_page = CheckoutOverviewPage(driver)

    with allure.step("Click continue button and navigate to overview page"):
        print("\nStep_06_Clicking_Continue_Button")
        info_page.click_continue()
        assert overview_page.is_overview_page_loaded(), "Failed to navigate to overview page"
        print("Step_06_Checkout_Overview_Page_Displayed")

        screenshot = Utility.capture_screenshot(driver, "Step_06_Checkout_Overview_Page_Displayed")
        allure.attach(screenshot,
                      name="Step_06_Checkout_Overview_Page_Displayed",
                      attachment_type=allure.attachment_type.PNG)

    return overview_page