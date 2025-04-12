import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Utility.utility import Utility


class ProductPage:
    # -------------------------------
    # Locators for the Products elements on the page
    # -------------------------------
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    # List of available products on the Sauce Demo site
    AVAILABLE_PRODUCTS = [
        "sauce-labs-backpack",
        "sauce-labs-bike-light",
        "sauce-labs-bolt-t-shirt",
        "sauce-labs-fleece-jacket",
        "sauce-labs-onesie",
        "test.allthethings()-t-shirt-(red)"
    ]

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.available_products = self.AVAILABLE_PRODUCTS.copy()

    def is_product_page_loaded(self):
        """
        Verify if the products page is loaded successfully.
        """
        try:
            return Utility.wait_for_element_visible(self.driver, self.INVENTORY_CONTAINER).is_displayed()
        except Exception:
            return False

    def add_product_to_cart(self, product_id):
        """
        Add the specified product to the shopping cart.
        """
        add_button_id = f"add-to-cart-{product_id}"
        try:
            # Wait for the add-to-cart button to be clickable
            add_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, add_button_id))
            )

            # Attempt to click the button up to three times
            for _ in range(3):
                try:
                    # Use JavaScript click for more reliability
                    self.driver.execute_script("arguments[0].click();", add_button)
                    # After clicking, wait for the corresponding remove button to appear as verification
                    self.wait.until(
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
            badge = self.driver.find_element(*self.SHOPPING_CART_BADGE)
            return int(badge.text)
        except Exception:
            return 0

    def go_to_cart(self):
        """
        Navigate to the cart page using JavaScript to click the cart icon.
        """
        try:
            cart_icon = self.driver.find_element(*self.SHOPPING_CART_LINK)
            self.driver.execute_script("arguments[0].click();", cart_icon)
            time.sleep(1)  # Pause briefly to allow the page transition
            print("Navigated to the cart page using JavaScript click.")
            return True
        except Exception as e:
            print(f"Error navigating to cart: {str(e)}")
            return False
