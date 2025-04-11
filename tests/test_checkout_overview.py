import allure


@allure.epic("Swag Labs E-commerce")
@allure.feature("Checkout Process")
@allure.story("Review order and complete purchase")
@allure.severity(allure.severity_level.CRITICAL)
def test_checkout_overview(overview_page_loaded):
    """Test checkout overview and order completion"""
    # Finish the order
    with allure.step("Complete checkout by clicking finish"):
        overview_page_loaded.click_finish()

        # Add assertions for order completion if needed