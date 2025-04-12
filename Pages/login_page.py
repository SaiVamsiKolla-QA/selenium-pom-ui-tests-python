from selenium.webdriver.common.by import By


class LoginPage:
    # -------------------------------
    # Locators for the login elements on the page
    # -------------------------------
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")

    def __init__(self, driver):
        self.driver = driver

    # -------------------------------
    # Page Actions: Methods to interact with the login page elements
    # -------------------------------
    def open_page(self, url):
        self.driver.get(url)

    def enter_username(self, username):
        self.driver.find_element(*self.USERNAME_FIELD).send_keys(username)

    def enter_password(self, password):
        self.driver.find_element(*self.PASSWORD_FIELD).send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def login_as(self, username, password, url):
        self.open_page(url)
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
