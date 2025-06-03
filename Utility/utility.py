import os
from datetime import datetime

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Utility:

    @staticmethod
    def get_browser_name(driver):
        """Get the current browser name from the driver capabilities."""
        capabilities = driver.capabilities
        browser_name = capabilities.get('browserName', '').lower()
        return browser_name



    @staticmethod
    def capture_screenshot(driver, test_name=None):
        """
        Capture a screenshot and save it in the assets/screenshots directory.
        Returns the screenshot as bytes for Allure reporting.
        """
        try:
            browser_name = Utility.get_browser_name(driver)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            name = f"{test_name}_{timestamp}" if test_name else f"screenshot_{timestamp}"

            screenshot_dir = os.path.join(os.getcwd(), "assets", "screenshots", browser_name)
            
            # Try to create directory if it doesn't exist
            try:
                if not os.path.exists(screenshot_dir):
                    os.makedirs(screenshot_dir, exist_ok=True)
            except PermissionError:
                print(f"Warning: Could not create screenshot directory: {screenshot_dir}")
                # Return screenshot bytes even if we can't save to file
                return driver.get_screenshot_as_png()

            # Try to save screenshot to file
            screenshot_path = os.path.join(screenshot_dir, f"{name}.png")
            try:
                driver.save_screenshot(screenshot_path)
                print(f"Screenshot saved to: {screenshot_path}")
            except Exception as e:
                print(f"Warning: Could not save screenshot to file: {e}")

            # Return screenshot bytes for Allure even if file save failed
            return driver.get_screenshot_as_png()
            
        except Exception as e:
            print(f"Error capturing screenshot: {e}")
            return None

    @staticmethod
    def wait_for_element_visible(driver, locator, timeout=10):
        """
        Wait until the element specified by the locator is visible.
        """
        # -------------------------------
        # Create a WebDriverWait and wait for the element to become visible
        # -------------------------------
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))

