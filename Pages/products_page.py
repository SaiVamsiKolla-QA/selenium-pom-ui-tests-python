import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utility.utility import Utility

class ProductPage:
    """
    Page object for the Products page of the Sauce Demo website.
    Implements the Page Object Model (POM) pattern.
    """

    def __init__(self, driver):
        self.driver = driver

        # Locators for the Products page
        self.inventory_container = (By.ID, "inventory_container")
        self.shopping_cart_badge = (By.CLASS_NAME, "shopping_cart_badge")

        # List of available products on the Sauce Demo site
        self.available_products = [
            "sauce-labs-backpack",
            "sauce-labs-bike-light",
            "sauce-labs-bolt-t-shirt",
            "sauce-labs-fleece-jacket",
            "sauce-labs-onesie",
            "test.allthethings()-t-shirt-(red)"
        ]

    def is_page_loaded(self):
        """
        Verify if the products page is loaded successfully.
        :return: True if the page is loaded, False otherwise
        """
        try:
            inventory_locator = (By.ID, "inventory_container")
            return Utility.wait_for_element_visible(self.driver, inventory_locator).is_displayed()
        except:
            return False

    def wait_for_page_load(self, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.inventory_container)
            )
            return True
        except Exception:
            return False

    def add_product_to_cart(self, product_id):
        add_button_id = f"add-to-cart-{product_id}"
        try:
            add_button = self.driver.find_element(By.ID, add_button_id)
            add_button.click()
            return True
        except Exception as e:
            print(f"Error: Could not add product {product_id}. Exception: {str(e)}")
            return False

    def get_cart_count(self):
        try:
            badge = self.driver.find_element(*self.shopping_cart_badge)
            return int(badge.text)
        except Exception:
            return 0

    # Alternative approach using JavaScript click
    def go_to_cart(self):
        try:
            cart_icon = self.driver.find_element(By.CLASS_NAME, "shopping_cart_link")
            self.driver.execute_script("arguments[0].click();", cart_icon)
            time.sleep(1)
            print("Navigated to the cart page using JavaScript click.")
            return True
        except Exception as e:
            print(f"Error navigating to cart: {str(e)}")
            return False
