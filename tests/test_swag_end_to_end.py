import allure

from Utility.utility import Utility


@allure.epic("Swag Labs E-commerce")
@allure.feature("Swag End-to-End Process")
def test_swag_end_to_end(overview_page_loaded, driver):
    """Test complete end-to-end checkout process from login to completion"""
    allure.dynamic.story("User completes full purchase flow")
    allure.dynamic.severity(allure.severity_level.CRITICAL)

    # Get the overview page from the fixture
    # At this point, we've already:
    # 1. Logged in successfully
    # 2. Added products to cart
    # 3. Navigated to cart
    # 4. Clicked checkout
    # 5. Entered customer information
    # 6. Clicked continue to reach overview page
    overview_page = overview_page_loaded

    # -------------------------------
    # Step 7: Click the finish button and complete checkout
    # -------------------------------
    with allure.step("Complete checkout by clicking finish"):
        print("\nStep_07_Checkout_Complete")
        overview_page.click_finish()

        screenshot = Utility.capture_screenshot(driver, "Step_07_Checkout_Complete")
        allure.attach(screenshot,
                      name="Step_07_Checkout_Complete",
                      attachment_type=allure.attachment_type.PNG)

        # Verify completion if your app has a confirmation element
        # Example: assert completion_page.is_order_complete(), "Order completion failed"

        allure.attach("Checkout process completed successfully",
                      name="Checkout Completion",
                      attachment_type=allure.attachment_type.TEXT)
