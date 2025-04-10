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
        try:
            inventory_locator = (By.ID, "inventory_container")
            return Utility.wait_for_element_visible(self.driver, inventory_locator).is_displayed()
        except:
            return False

    def add_product_to_cart(self, product_id):
        add_button_id = f"add-to-cart-{product_id}"
        try:
            # Wait for the button to be clickable
            add_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.ID, add_button_id))
            )

            # Scroll to the button to ensure it's in view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
            time.sleep(0.5)  # Small pause after scrolling

            # Try regular click first
            try:
                add_button.click()
            except Exception:
                # If regular click fails, try JavaScript click
                self.driver.execute_script("arguments[0].click();", add_button)

            # Verify the item was added by checking for the REMOVE button
            remove_button_id = f"remove-{product_id}"
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.ID, remove_button_id))
            )

            print(f"Successfully added {product_id} to cart")
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

    #  Using JavaScript to click on cart
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
