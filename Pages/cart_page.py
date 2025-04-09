from selenium.webdriver.common.by import By
from Pages.base_page import BasePage


class CartPage(BasePage):
    """
    Page object for the shopping cart page of the Sauce Demo website.
    This implementation includes only the essential methods needed to
    verify items in the cart and proceed to checkout.
    """

    # -------------------------------
    # Locators for cart elements
    # -------------------------------
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def __init__(self, driver):
        """
        Initialize the CartPage with a WebDriver instance.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
        """
        super().__init__(driver)

    def click_checkout(self):
        """
        Click the checkout button to initiate the checkout process.

        Returns:
            bool: True if the checkout button was successfully clicked, False otherwise.
        """
        # -------------------------------
        # Click the checkout button using the BasePage's click_element method
        # -------------------------------
        try:
            return self.click_element(self.CHECKOUT_BUTTON)
        except Exception as e:
            print(f"Error clicking the checkout button: {str(e)}")
            return False

