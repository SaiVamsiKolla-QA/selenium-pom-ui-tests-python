from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
            print(f"Added product to cart: {product_id}")
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

    def go_to_cart(self):
        """
        Clicks the shopping cart link to navigate to the cart page.
        """
        # Optionally add an explicit wait to ensure the element is clickable:
        cart_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))
        )
        cart_link.click()
        print("Navigated to the cart page.")
