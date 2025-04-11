from selenium.webdriver.common.by import By

from Pages.base_page import BasePage
from Utility.utility import Utility


class CheckoutInfoPage(BasePage):
    """
    Page object for the checkout information page (step one) of the Sauce Demo website.
    This page handles entering customer information during the checkout process.
    """

    # Locators for checkout information page elements
    FIRST_NAME_FIELD = (By.ID, "first-name")
    LAST_NAME_FIELD = (By.ID, "last-name")
    POSTAL_CODE_FIELD = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CHECKOUT_INFO_TITLE = (By.CLASS_NAME, "title")

    def __init__(self, driver):
        super().__init__(driver)

    def is_info_page_loaded(self):
        # Your existing implementation remains here.
        try:
            info_title_locator = (By.CLASS_NAME, "title")
            continue_button_locator = (By.ID, "continue")
            title_element = Utility.wait_for_element_visible(self.driver, info_title_locator)
            if not (title_element.is_displayed() and title_element.text == "Checkout: Your Information"):
                return False
            continue_button = Utility.wait_for_element_visible(self.driver, continue_button_locator)
            return continue_button.is_displayed()
        except Exception as e:
            print(f"Error in is_info_page_loaded: {str(e)}")
            return False

    def enter_first_name(self, first_name):
        self.driver.find_element(*self.FIRST_NAME_FIELD).send_keys(first_name)

    def enter_last_name(self, last_name):
        element = self.driver.find_element(*self.LAST_NAME_FIELD)
        element.clear()
        element.send_keys(last_name)

    def enter_postal_code(self, postal_code):
        element = self.driver.find_element(*self.POSTAL_CODE_FIELD)
        element.clear()
        element.send_keys(postal_code)

    def click_continue(self):
        self.driver.find_element(*self.CONTINUE_BUTTON).click()

    def get_first_name(self):
        return self.driver.find_element(*self.FIRST_NAME_FIELD).get_attribute("value")

    def get_last_name(self):
        return self.driver.find_element(*self.LAST_NAME_FIELD).get_attribute("value")

    def get_postal_code(self):
        return self.driver.find_element(*self.POSTAL_CODE_FIELD).get_attribute("value")

    def verify_checkout_information(self, first_name, last_name, postal_code):
        """
        Verify that the checkout information fields contain the expected values.
        """
        assert self.get_first_name() == first_name, f"Expected first name to be '{first_name}', but got '{self.get_first_name()}'"
        assert self.get_last_name() == last_name, f"Expected last name to be '{last_name}', but got '{self.get_last_name()}'"
        assert self.get_postal_code() == postal_code, f"Expected postal code to be '{postal_code}', but got '{self.get_postal_code()}'"