from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """
    Base class for all page objects with common utilities and methods.
    This class implements common functionality that will be reused across different pages.
    """

    def __init__(self, driver):
        """
        Initialize the base page with a WebDriver instance.

        """
        self.driver = driver
        self.default_timeout = 10

    def open_url(self, url):
        """
        Open a specific URL in the browser.
        """
        self.driver.get(url)

    def find_element(self, locator, timeout=None):
        """
        Find an element on the page, with configurable timeout.
        """
        if timeout is None:
            timeout = self.default_timeout

        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            raise NoSuchElementException(f"Element not found with locator {locator}")

    def click_element(self, locator, timeout=None):
        """
        Find and click an element on the page.
        """
        try:
            element = self.find_element(locator, timeout)
            element.click()
            return True
        except Exception as e:
            print(f"Failed to click element {locator}: {str(e)}")
            return False

    def enter_text(self, locator, text, timeout=None):
        """
        Find an element and enter text into it.
        """
        try:
            element = self.find_element(locator, timeout)
            element.clear()
            element.send_keys(text)
            return True
        except Exception as e:
            print(f"Failed to enter text in element {locator}: {str(e)}")
            return False

    def get_element_text(self, locator, timeout=None):
        """
        Get the text from an element.
        """
        try:
            element = self.find_element(locator, timeout)
            return element.text
        except Exception as e:
            print(f"Failed to get text from element {locator}: {str(e)}")
            return None

    def is_element_present(self, locator, timeout=5):
        """
        Check if an element is present on the page.
        """
        try:
            self.find_element(locator, timeout)
            return True
        except NoSuchElementException:
            return False

    def wait_for_page_load(self, timeout=None):
        """
        Wait for the page to finish loading.
        """
        if timeout is None:
            timeout = self.default_timeout

        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            return True
        except TimeoutException:
            print("Page did not load completely within the timeout period")
            return False
