from selenium.webdriver.common.by import By

from Pages.base_page import BasePage
from Utility.utility import Utility


class CheckoutOverviewPage(BasePage):
    # -------------------------------
    # Locators for checkout overview page elements
    # -------------------------------
    CHECKOUT_OVERVIEW_TITLE = (By.CLASS_NAME, "title")
    FINISH_BUTTON = (By.ID, "finish")

    def __init__(self, driver):
        super().__init__(driver)

    def is_overview_page_loaded(self):
        try:
            # -------------------------------
            # Wait for the overview page title element to be visible.
            # -------------------------------
            title_element = Utility.wait_for_element_visible(self.driver, self.CHECKOUT_OVERVIEW_TITLE)
            # Verify that the title is displayed and matches the expected text.
            if not (title_element.is_displayed() and title_element.text.strip() == "Checkout: Overview"):
                print(f"Overview title mismatch. Found: '{title_element.text}'")
                return False

            # -------------------------------
            # Wait for the finish button element to be visible.
            # -------------------------------
            finish_button = Utility.wait_for_element_visible(self.driver, self.FINISH_BUTTON)
            if not finish_button.is_displayed():
                print("Finish button is not displayed.")
            return finish_button.is_displayed()
        except Exception as e:
            print(f"Error in is_overview_page_displayed: {str(e)}")
            return False

    def click_finish(self):
        try:
            # -------------------------------
            # Wait for the finish button to be visible.
            # -------------------------------
            finish_button = Utility.wait_for_element_visible(self.driver, self.FINISH_BUTTON)
            # Scroll the finish button into view.
            self.driver.execute_script("arguments[0].scrollIntoView(true);", finish_button)
            # Attempt a normal click.
            finish_button.click()
            print("Finish button clicked successfully using a normal click.")
            return True
        except Exception as e:
            print(f"Normal click failed on finish button: {str(e)}")
            try:
                # -------------------------------
                # Fallback: Use JavaScript to click the finish button.
                # -------------------------------
                finish_button = self.driver.find_element(*self.FINISH_BUTTON)
                self.driver.execute_script("arguments[0].click();", finish_button)
                print("Finish button clicked successfully using JavaScript.")
                return True
            except Exception as e:
                print(f"JavaScript click failed on finish button: {str(e)}")
                return False
