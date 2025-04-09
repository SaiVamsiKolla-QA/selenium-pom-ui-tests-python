from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

class LoginPage:
    # -------------------------------
    # Locators for the login elements on the page
    # -------------------------------
    def __init__(self, driver):
        self.driver = driver
        self.username_field = (By.ID, "user-name")
        self.password_field = (By.ID, "password")
        self.login_button = (By.ID, "login-button")

    # -------------------------------
    # Page Actions: Methods to interact with the login page elements
    # -------------------------------
    def open_page(self, url):
        """
        Open the specified URL in the current browser window.
        :param url: The URL to navigate to.
        """
        self.driver.get(url)

    def enter_username(self, username):
        """
        Locate the username field and enter the provided username.
        :param username: The username string to be entered.
        """
        self.driver.find_element(*self.username_field).send_keys(username)

    def enter_password(self, password):
        """
        Locate the password field and enter the provided password.
        :param password: The password string to be entered.
        """
        self.driver.find_element(*self.password_field).send_keys(password)

    def click_login(self):
        """
        Locate the login button and perform a click action.
        """
        self.driver.find_element(*self.login_button).click()

    # -------------------------------
    # Convenience Method: Login using a single method call
    # This method encapsulates the complete login sequence:
    #   1. Open the specified URL.
    #   2. Enter username and password.
    #   3. Click the login button.
    # -------------------------------
    def login_as(self, username, password, url="https://www.saucedemo.com/"):
        """
        Perform a complete login flow using the provided credentials.
        :param username: The username for login.
        :param password: The password for login.
        :param url: The URL of the login page (defaults to Sauce Demo URL).
        """
        self.open_page(url)
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
