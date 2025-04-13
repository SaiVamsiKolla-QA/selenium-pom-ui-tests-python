import allure


@allure.epic("Swag Labs E-commerce")
@allure.feature("Checkout Overview")
@allure.story("Review order and complete purchase")
@allure.severity(allure.severity_level.CRITICAL)
def test_swag_checkout_step_two(overview_page_loaded):
    """Test checkout overview and order completion"""
    # Finish the order
    with allure.step("Complete checkout by clicking finish"):
        overview_page_loaded.click_finish()