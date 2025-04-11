import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from Pages.base_page import BasePage


class CheckoutInfoPage(BasePage):
    """Checkout information page with enhanced text persistence"""

    # Locators (keep original names)
    FIRST_NAME_FIELD = (By.ID, "first-name")
    LAST_NAME_FIELD = (By.ID, "last-name")
    POSTAL_CODE_FIELD = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CHECKOUT_INFO_TITLE = (By.CLASS_NAME, "title")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)
        self.actions = ActionChains(driver)

    def is_info_page_loaded(self):
        """Verify if page is loaded with all critical elements"""
        try:
            title_visible = EC.text_to_be_present_in_element(
                self.CHECKOUT_INFO_TITLE, "Checkout: Your Information"
            )(self.driver)
            button_visible = EC.element_to_be_clickable(self.CONTINUE_BUTTON)(self.driver)
            return title_visible and button_visible
        except TimeoutException:
            return False

    def _persistent_text_entry(self, locator, value, attempts=3):
        """Robust text entry with event triggering and validation"""
        element = self.wait.until(EC.presence_of_element_located(locator))
        for attempt in range(attempts):
            try:
                # Scroll and focus
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                self.actions.move_to_element(element).pause(0.2).perform()

                # Clear existing value with events
                self.driver.execute_script("""
                    arguments[0].value = '';
                    arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                    arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                """, element)

                # Physical text entry
                element.click()
                element.send_keys(value)

                # Trigger field blur
                element.send_keys(Keys.TAB)
                time.sleep(0.3)

                # Verify persistence
                self.wait.until(lambda d: element.get_attribute("value") == value)
                return True
            except Exception:
                # JavaScript fallback with events
                self.driver.execute_script("""
                    arguments[0].value = arguments[1];
                    arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                    arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                """, element, value)
                time.sleep(0.3)
                if element.get_attribute("value") == value:
                    return True
                if attempt == attempts - 1:
                    raise
                time.sleep(0.5)

    def enter_first_name(self, first_name):
        return self._persistent_text_entry(self.FIRST_NAME_FIELD, first_name)

    def enter_last_name(self, last_name):
        return self._persistent_text_entry(self.LAST_NAME_FIELD, last_name)

    def enter_postal_code(self, postal_code):
        return self._persistent_text_entry(self.POSTAL_CODE_FIELD, postal_code)

    def click_continue(self):
        """Click continue with pre-click validation"""
        # Verify all fields have persisted values
        fields = [self.FIRST_NAME_FIELD, self.LAST_NAME_FIELD, self.POSTAL_CODE_FIELD]
        for field in fields:
            element = self.wait.until(EC.presence_of_element_located(field))
            if not element.get_attribute("value"):
                raise ValueError(f"Field {field} is empty before continuing")

        # Perform click
        for _ in range(3):
            try:
                btn = self.wait.until(EC.element_to_be_clickable(self.CONTINUE_BUTTON))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)

                # Click with verification
                self.driver.execute_script("arguments[0].click();", btn)
                time.sleep(0.5)

                # Wait for next page
                WebDriverWait(self.driver, 10).until(
                    EC.invisibility_of_element_located(self.CHECKOUT_INFO_TITLE)
                )
                return True
            except Exception:
                time.sleep(0.5)
        return False

    # Keep original get_* methods and verify_checkout_information
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
        # ... rest of the verification logic ...

    def _get_field_value(self, locator):
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            return element.get_attribute("value")
        except TimeoutException:
            return None