from selenium.webdriver.common.by import By

from .base_page import BasePage


class LoginPage(BasePage):
    # -------------------------------
    # Locators for the login elements on the page
    # -------------------------------
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")

    # -------------------------------
    # Page Actions: Methods to interact with the login page elements
    # -------------------------------
    def enter_username(self, username):
        self.driver.find_element(*self.USERNAME_FIELD).send_keys(username)

    def enter_password(self, password):
        self.driver.find_element(*self.PASSWORD_FIELD).send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def login_as(self, username, password, url):
        self.open_url(url)  # This uses the inherited method from BasePage
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
