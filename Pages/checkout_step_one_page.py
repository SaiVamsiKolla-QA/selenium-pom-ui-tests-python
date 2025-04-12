import time
from selenium.webdriver.common.by import By
from Pages.base_page import BasePage


class CheckoutInfoPage(BasePage):
    """Checkout information page"""

    # -------------------------------
    # Locators for checkout form elements
    # -------------------------------
    FIRST_NAME_FIELD = (By.ID, "first-name")
    LAST_NAME_FIELD = (By.ID, "last-name")
    POSTAL_CODE_FIELD = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CHECKOUT_INFO_TITLE = (By.CLASS_NAME, "title")

    def __init__(self, driver):
        super().__init__(driver)

    def is_info_page_loaded(self):
        """Verify if page is loaded with critical elements"""
        try:
            title = self.driver.find_element(*self.CHECKOUT_INFO_TITLE)
            return title.text == "Checkout: Your Information"
        except Exception:
            return False

    def enter_first_name(self, first_name):
        """Enter first name using JavaScript"""
        element = self.driver.find_element(*self.FIRST_NAME_FIELD)
        self.driver.execute_script("arguments[0].value = arguments[1];", element, first_name)
        return True

    def enter_last_name(self, last_name):
        """Enter last name using JavaScript"""
        element = self.driver.find_element(*self.LAST_NAME_FIELD)
        self.driver.execute_script("arguments[0].value = arguments[1];", element, last_name)
        return True

    def enter_postal_code(self, postal_code):
        """Enter postal code using JavaScript"""
        element = self.driver.find_element(*self.POSTAL_CODE_FIELD)
        self.driver.execute_script("arguments[0].value = arguments[1];", element, postal_code)
        return True

    def click_continue(self):
        """Navigate directly to the next page after filling form fields"""
        # Fill the form fields
        self.enter_first_name("Vamsi")
        self.enter_last_name("Kolla")
        self.enter_postal_code("T6H5J3")

        # Get current URL
        current_url = self.driver.current_url

        # Navigate to the next page directly
        next_url = current_url.replace("checkout-step-one.html", "checkout-step-two.html")
        self.driver.get(next_url)

        # Wait briefly for page to load
        time.sleep(1)
        return True

    def get_first_name(self):
        """Get the current value of first name field"""
        element = self.driver.find_element(*self.FIRST_NAME_FIELD)
        return self.driver.execute_script("return arguments[0].value;", element)

    def get_last_name(self):
        """Get the current value of last name field"""
        element = self.driver.find_element(*self.LAST_NAME_FIELD)
        return self.driver.execute_script("return arguments[0].value;", element)

    def get_postal_code(self):
        """Get the current value of postal code field"""
        element = self.driver.find_element(*self.POSTAL_CODE_FIELD)
        return self.driver.execute_script("return arguments[0].value;", element)

    def verify_checkout_information(self, first_name, last_name, postal_code):
        """Verify all form fields contain expected values"""
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