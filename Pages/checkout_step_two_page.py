from selenium.webdriver.common.by import By
from Pages.base_page import BasePage


class CheckoutOverviewPage(BasePage):
    """Checkout overview page"""

    # -------------------------------
    # Locators for checkout overview page elements
    # -------------------------------
    CHECKOUT_OVERVIEW_TITLE = (By.CLASS_NAME, "title")
    FINISH_BUTTON = (By.ID, "finish")

    def __init__(self, driver):
        super().__init__(driver)

    def is_overview_page_loaded(self):
        """Verify if overview page is loaded with critical elements"""
        try:
            title = self.driver.find_element(*self.CHECKOUT_OVERVIEW_TITLE)
            is_title_correct = title.text == "Checkout: Overview"

            if not is_title_correct:
                print(f"Overview title mismatch. Found: '{title.text}'")
                return False

            finish_button = self.driver.find_element(*self.FINISH_BUTTON)
            return finish_button.is_displayed()
        except Exception:
            return False

    def click_finish(self):
        """Click the finish button using JavaScript for reliability"""
        finish_button = self.driver.find_element(*self.FINISH_BUTTON)
        self.driver.execute_script("arguments[0].click();", finish_button)
        return True