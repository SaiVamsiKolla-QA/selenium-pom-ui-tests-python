from selenium.webdriver.common.by import By

from .base_page import BasePage


class LoginPage(BasePage):
    # Page elements
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")

    def enter_username(self, username):
        """Enter username in the login form"""
        self.driver.find_element(*self.USERNAME_FIELD).send_keys(username)

    def enter_password(self, password):
        """Enter password in the login form"""
        self.driver.find_element(*self.PASSWORD_FIELD).send_keys(password)

    def click_login(self):
        """Click the login button"""
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def login(self, username, password):
        """Perform complete login action"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
