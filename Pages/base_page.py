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

        Args:
            driver: The Selenium WebDriver instance to use for browser interactions
        """
        self.driver = driver
        self.default_timeout = 10

    def open_url(self, url):
        """
        Open a specific URL in the browser.

        Args:
            url: The URL to open
        """
        self.driver.get(url)

    def find_element(self, locator, timeout=None):
        """
        Find an element on the page, with configurable timeout.

        Args:
            locator: A tuple of (By strategy, selector string)
            timeout: Optional timeout in seconds (uses default_timeout if not specified)

        Returns:
            The WebElement if found, raises exception otherwise
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

        Args:
            locator: A tuple of (By strategy, selector string)
            timeout: Optional timeout in seconds

        Returns:
            True if the click was successful, False otherwise
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

        Args:
            locator: A tuple of (By strategy, selector string)
            text: The text to enter
            timeout: Optional timeout in seconds

        Returns:
            True if text entry was successful, False otherwise
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

        Args:
            locator: A tuple of (By strategy, selector string)
            timeout: Optional timeout in seconds

        Returns:
            The text content of the element, or None if not found
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

        Args:
            locator: A tuple of (By strategy, selector string)
            timeout: Optional timeout in seconds (shorter timeout is better for checking presence)

        Returns:
            True if the element is present, False otherwise
        """
        try:
            self.find_element(locator, timeout)
            return True
        except NoSuchElementException:
            return False

    def wait_for_page_load(self, timeout=None):
        """
        Wait for the page to finish loading.

        Args:
            timeout: Optional timeout in seconds

        Returns:
            True if the page loaded within the timeout, False otherwise
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

    def take_screenshot(self, filename):
        """
        Take a screenshot and save it with the given filename.

        Args:
            filename: Name to save the screenshot as (without extension)

        Returns:
            Path to the saved screenshot, or None if failed
        """
        try:
            screenshot_path = f"screenshots/{filename}.png"
            self.driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")
            return screenshot_path
        except Exception as e:
            print(f"Failed to take screenshot: {str(e)}")
            return None
