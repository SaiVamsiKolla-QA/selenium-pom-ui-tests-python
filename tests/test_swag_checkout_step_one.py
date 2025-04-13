import allure


@allure.epic("Swag Labs E-commerce")
@allure.feature("Swag Checkout Page One")
def test_swag_checkout_step_one(checkout_info_filled, driver):
    """Test completing checkout information and navigating to overview page"""
    allure.dynamic.story("User enter the necessary details to complete the check out process")
    allure.dynamic.severity(allure.severity_level.CRITICAL)

    # Get the info page from the fixture
    info_page = checkout_info_filled

    # Create overview page
    from Pages.checkout_step_two_page import CheckoutOverviewPage
    overview_page = CheckoutOverviewPage(driver)

    # -------------------------------
    # Step 6: Click continue to proceed to overview
    # -------------------------------
    with allure.step("Click continue to proceed to overview"):
        info_page.click_continue()
        assert overview_page.is_overview_page_loaded(), "Failed to navigate to overview page"

        from Utility.utility import Utility
        screenshot = Utility.capture_screenshot(driver, "Step_06_Checkout_Overview_Page_Displayed")
        allure.attach(screenshot,
                      name="Step_06_Checkout_Overview_Page_Displayed",
                      attachment_type=allure.attachment_type.PNG)

        print("\nStep_06_Checkout_Overview_Page_Displayed")