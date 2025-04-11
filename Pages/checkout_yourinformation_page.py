import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from Pages.base_page import BasePage


class CheckoutInfoPage(BasePage):
    """Checkout information page"""

    # Locators
    FIRST_NAME_FIELD = (By.ID, "first-name")
    LAST_NAME_FIELD = (By.ID, "last-name")
    POSTAL_CODE_FIELD = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CHECKOUT_INFO_TITLE = (By.CLASS_NAME, "title")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)

    def is_info_page_loaded(self):
        """Verify if page is loaded with critical elements"""
        try:
            title_visible = EC.text_to_be_present_in_element(
                self.CHECKOUT_INFO_TITLE, "Checkout: Your Information"
            )(self.driver)
            button_visible = EC.element_to_be_clickable(self.CONTINUE_BUTTON)(self.driver)
            return title_visible and button_visible
        except TimeoutException:
            return False

    def _persistent_text_entry(self, locator, value):
        """Simple text entry with validation"""
        element = self.wait.until(EC.presence_of_element_located(locator))

        # Clear and enter text
        element.clear()
        element.send_keys(value)

        # Verify text was entered
        return element.get_attribute("value") == value

    def enter_first_name(self, first_name):
        return self._persistent_text_entry(self.FIRST_NAME_FIELD, first_name)

    def enter_last_name(self, last_name):
        return self._persistent_text_entry(self.LAST_NAME_FIELD, last_name)

    def enter_postal_code(self, postal_code):
        return self._persistent_text_entry(self.POSTAL_CODE_FIELD, postal_code)

    def click_continue(self):
        """Click continue button"""
        try:
            btn = self.wait.until(EC.element_to_be_clickable(self.CONTINUE_BUTTON))
            btn.click()

            # Wait for page transition
            self.wait.until(EC.invisibility_of_element_located(self.CHECKOUT_INFO_TITLE))
            return True
        except TimeoutException:
            return False

    def get_first_name(self):
        return self._get_field_value(self.FIRST_NAME_FIELD)

    def get_last_name(self):
        return self._get_field_value(self.LAST_NAME_FIELD)

    def get_postal_code(self):
        return self._get_field_value(self.POSTAL_CODE_FIELD)

    def verify_checkout_information(self, first_name, last_name, postal_code):
        current_values = {
            'first_name': self.get_first_name(),
            'last_name': self.get_last_name(),
            'postal_code': self.get_postal_code()
        }

        expected_values = {
            'first_name': first_name,
            'last_name': last_name,
            'postal_code': postal_code
        }

        return current_values == expected_values

    def _get_field_value(self, locator):
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            return element.get_attribute("value")
        except TimeoutException:
            return None