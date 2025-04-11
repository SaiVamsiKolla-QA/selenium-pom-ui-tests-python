import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Utility.utility import Utility


class ProductPage:
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

    def is_product_page_loaded(self):
        """
         Verify if the products page is loaded successfully.
        """
        try:
            inventory_locator = (By.ID, "inventory_container")
            return Utility.wait_for_element_visible(self.driver, inventory_locator).is_displayed()
        except Exception:
            return False

    def add_product_to_cart(self, product_id):
        """
        Add the specified product to the shopping cart.
        """
        add_button_id = f"add-to-cart-{product_id}"
        try:
            # Wait for the add-to-cart button to be clickable.
            add_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, add_button_id))
            )

            # Attempt to click the button up to three times.
            for _ in range(3):
                try:
                    # Use JavaScript click for more reliability.
                    self.driver.execute_script("arguments[0].click();", add_button)
                    # After clicking, wait for the corresponding remove button to appear as verification.
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.ID, f"remove-{product_id}"))
                    )
                    return True
                except Exception:
                    continue
            return False
        except Exception as e:
            print(f"Critical error adding product: {str(e)}")
            return False

    def get_cart_count(self):
        """
        Retrieve the number of items in the shopping cart.
        """
        try:
            badge = self.driver.find_element(*self.shopping_cart_badge)
            return int(badge.text)
        except Exception:
            return 0

    def go_to_cart(self):
        """
        Navigate to the cart page using JavaScript to click the cart icon.
        """
        try:
            cart_icon = self.driver.find_element(By.CLASS_NAME, "shopping_cart_link")
            self.driver.execute_script("arguments[0].click();", cart_icon)
            time.sleep(1)  # Pause briefly to allow the page transition.
            print("Navigated to the cart page using JavaScript click.")
            return True
        except Exception as e:
            print(f"Error navigating to cart: {str(e)}")
            return False
