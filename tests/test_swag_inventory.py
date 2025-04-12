import allure


@allure.epic("Swag Labs E-commerce")
@allure.feature("Product Management")
@allure.story("Add products to cart")
@allure.severity(allure.severity_level.CRITICAL)
def test_swag_inventory(products_added_to_cart):
    """Test adding 2 random products to cart"""
    # Just verify the fixture worked properly
    product_page, products_to_add = products_added_to_cart
    assert product_page.get_cart_count() == len(products_to_add)
