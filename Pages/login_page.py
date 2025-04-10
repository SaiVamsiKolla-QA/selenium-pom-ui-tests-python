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
        self.driver.get(url)

    def enter_username(self, username):
        self.driver.find_element(*self.username_field).send_keys(username)

    def enter_password(self, password):
        self.driver.find_element(*self.password_field).send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.login_button).click()

    # -------------------------------
    #   1. Open the specified URL.
    #   2. Enter username and password.
    #   3. Click the login button.
    # -------------------------------
    def login_as(self, username, password, url="https://www.saucedemo.com/"):
        self.open_page(url)
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
