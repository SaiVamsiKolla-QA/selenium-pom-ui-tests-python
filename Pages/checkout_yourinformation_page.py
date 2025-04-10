from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys  # Add this import
from Pages.base_page import BasePage
from Utility.utility import Utility


class CheckoutInfoPage(BasePage):
    """
    Page object for the checkout information page (step one) of the Sauce Demo website.
    This page handles entering customer information during the checkout process.
    """

    # -------------------------------
    # Locators for checkout information page elements
    # -------------------------------
    FIRST_NAME_FIELD = (By.ID, "first-name")
    LAST_NAME_FIELD = (By.ID, "last-name")
    POSTAL_CODE_FIELD = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CHECKOUT_INFO_TITLE = (By.CLASS_NAME, "title")

    def __init__(self, driver):
        """
        Initialize the CheckoutInfoPage with a WebDriver instance.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
        """
        super().__init__(driver)

    def is_info_page_displayed(self):
        """
        Verify if the checkout information page is loaded successfully.

        :return: True if the page is loaded (i.e., the title "Checkout: Your Information"
                 is visible and the continue button is displayed), False otherwise.
        """
        try:
            # -------------------------------
            # Define locators for the checkout information page.
            # -------------------------------
            info_title_locator = (By.CLASS_NAME, "title")
            continue_button_locator = (By.ID, "continue")

            # -------------------------------
            # Wait for the title element to be visible.
            # -------------------------------
            title_element = Utility.wait_for_element_visible(self.driver, info_title_locator)
            # Check if the title element is visible and its text matches the expected text.
            if not (title_element.is_displayed() and title_element.text == "Checkout: Your Information"):
                return False

            # -------------------------------
            # Wait for the continue button to be visible.
            # -------------------------------
            continue_button = Utility.wait_for_element_visible(self.driver, continue_button_locator)
            return continue_button.is_displayed()
        except Exception as e:
            print(f"Error in is_info_page_displayed: {str(e)}")
            return False

    def enter_first_name(self, first_name):
        """
        Enter the customer's first name using ActionChains for better form interaction.

        Args:
            first_name (str): The first name to enter

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Try with ActionChains for more reliable input
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.FIRST_NAME_FIELD)
            )
            element.clear()

            # Click to ensure focus
            element.click()

            # Send the full postal code string at once.
            element.send_keys(first_name)

            # Add a tab to trigger any blur events
            element.send_keys(Keys.TAB)

            return True
        except Exception as e:
            print(f"Error entering first name: {str(e)}")
            return False

    def enter_last_name(self, last_name):
        """
        Enter the customer's last name using ActionChains for better form interaction.

        Args:
            last_name (str): The last name to enter

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Try with ActionChains for more reliable input
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.LAST_NAME_FIELD)
            )
            element.clear()

            # Click to ensure focus
            element.click()

            # Send the full postal code string at once.
            element.send_keys(last_name)

            # Add a tab to trigger any blur events
            element.send_keys(Keys.TAB)

            return True
        except Exception as e:
            print(f"Error entering last name: {str(e)}")
            return False

    def enter_postal_code(self, postal_code):
        """
        Enter the customer's postal code by sending the complete string at once.

        Args:
            postal_code (str): The postal code to enter.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            # Wait until the postal code field is clickable.
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.POSTAL_CODE_FIELD)
            )
            element.clear()  # Clear any pre-existing text

            # Click the element to ensure focus.
            element.click()

            # Send the full postal code string at once.
            element.send_keys(postal_code)

            # Send TAB key to trigger any blur events.
            element.send_keys(Keys.TAB)

            return True
        except Exception as e:
            print(f"Error entering postal code: {str(e)}")
            return False

    def click_continue(self):
        """
        Click the continue button to proceed to the next checkout step.

        Returns:
            bool: True if the continue button was successfully clicked, False otherwise
        """
        try:
            # Wait for button to be clickable
            continue_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.CONTINUE_BUTTON)
            )

            # Click with explicit wait
            continue_button.click()
            return True
        except Exception as e:
            print(f"Error clicking continue button: {str(e)}")
            return False