import shutil
import tempfile

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from Pages.login_page import LoginPage
from Pages.products_page import ProductPage
from Utility.utility import Utility


@pytest.fixture(scope='function')
def driver():
    """
    Initialize and configure the Chrome WebDriver.
    """
    # Create a unique temporary directory for Chrome's user data
    user_data_dir = tempfile.mkdtemp(prefix="chrome_userdata_")
    print(f"[DEBUG] Using Chrome user-data-dir: {user_data_dir}")
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


@pytest.mark.parametrize("username,password", [
    ("standard_user", "secret_sauce"),
    ("locked_out_user", "secret_sauce"),
    ("problem_user", "secret_sauce"),
    (" performance_glitch_user", "secret_sauce"),
    ("error_user", "secret_sauce"),
    ("visual_user", "secret_sauce"),
])
@allure.epic("Swag Labs E-commerce")
@allure.feature('Swag Login Feature')
def test_swag_login(driver, username, password):
    """Test login functionality and verify the product page."""
    allure.dynamic.story(f"User {username} logs in")

    login_page = LoginPage(driver)
    product_page = ProductPage(driver)

    # -------------------------------
    # Step 1: Perform Login using provided credentials.
    # -------------------------------
    with allure.step(f"Login as {username}"):
        login_page.login_as(username, password, url="https://www.saucedemo.com/")

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
