import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from Pages.login_page import LoginPage
from Pages.products_page import ProductPage
from Utility.utility import Utility

@pytest.fixture()
def driver():
    # -------------------------------
    # Initialize and configure the WebDriver
    # -------------------------------
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.implicitly_wait(10)  # Set implicit wait for element loading
    yield driver
    # -------------------------------
    # Cleanup: Close and quit the WebDriver session
    # -------------------------------
    driver.close()  # Close the current browser window
    driver.quit()   # Quit the WebDriver and release resources


@pytest.mark.parametrize("username,password", [
    # -------------------------------
    # Test data: Standard user credentials expected to log in successfully
    # -------------------------------
    ("standard_user", "secret_sauce"),
])
def test_swag_login(driver, username, password):
    login_page = LoginPage(driver)
    product_page = ProductPage(driver)
    # -------------------------------
    # Step 1: Perform Login using provided credentials.
    # The login_as method encapsulates:
    #   - Navigating to the Sauce Demo website
    #   - Entering the username and password
    #   - Clicking the login button
    # -------------------------------
    login_page.login_as(username, password, url="https://www.saucedemo.com/")
    # -------------------------------
    # Step 2: Post-Login Actions
    #   - Capture a screenshot after the login attempt.
    #   - Wait for the inventory container element to verify successful login.
    # -------------------------------

    assert product_page.is_page_loaded(), f"Login failed for {username}"
    print(f"\nStep_01_Login_Successful_{username}")
    Utility.capture_screenshot(driver, f"Step_01_Login_Successful_{username}")

