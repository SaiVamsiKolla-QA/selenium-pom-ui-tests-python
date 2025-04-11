import allure

@allure.epic("Swag Labs E-commerce")
@allure.feature("Shopping Cart")
@allure.story("Navigate to cart and checkout")
@allure.severity(allure.severity_level.CRITICAL)
def test_cart_checkout(checkout_info_page_loaded):
    """Test cart navigation and proceeding to checkout"""
    # The fixture handles navigation to cart and checkout
    # We just need to verify we reached the info page
    assert checkout_info_page_loaded.is_info_page_loaded()