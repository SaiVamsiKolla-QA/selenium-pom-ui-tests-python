import os
import allure # Make sure allure is imported
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions


def pytest_addoption(parser):
    """
      Pytest hook that adds custom command-line options
      This allows us to specify which browser to use when running tests
    """
    parser.addoption("--browser", default="chrome",
                     help="Browser to run tests: chrome, firefox, edge, safari")
    parser.addoption("--remote-url", default=None,
                     help="Remote Selenium Grid URL (e.g., http://localhost:4444/wd/hub)")

@pytest.fixture(scope="session")
def browser_name(request):
    """
        Session-scoped fixture that retrieves the browser name from command line arguments.
        The 'session' scope means this value is calculated once per test session.
        It now includes an Allure step to log the selected browser.
    """
    # Retrieve the browser name from command line option
    selected_browser = request.config.getoption("--browser").lower()

    # Add an Allure step to make the selected browser visible in the fixture's execution
    with allure.step(f"Session Browser: {selected_browser.capitalize()}"):
        # This step will appear under 'browser_name' in the Allure report's "Set up" section
        pass # The step itself doesn't need to do more; its title is the key

    return selected_browser # Return the actual browser name for other fixtures/tests

@pytest.fixture(scope="function")
def allure_browser_param_fixture(browser_name):
    """
    Adds the browser name as a dynamic parameter to Allure reports for each test.
    This helps identify the browser used for a specific test in combined reports.
    """
    if browser_name:
        allure.dynamic.parameter("Browser Used", browser_name.capitalize())
    return browser_name

@pytest.fixture
def base_url():
    return "https://www.saucedemo.com/"

@pytest.fixture(scope='function')
def driver(browser_name, request): # Added 'request'
    """Initialize and configure the WebDriver based on browser selection and remote URL."""
    remote_url = request.config.getoption("--remote-url")
    is_ci = os.environ.get('CI') == 'true' or os.environ.get('GITHUB_ACTIONS') == 'true'

    if remote_url:
        # Logic for remote driver
        if browser_name == "chrome":
            options = ChromeOptions()
            if is_ci: # Apply CI options if needed for remote too
                options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")
        elif browser_name == "firefox":
            options = FirefoxOptions()
            if is_ci:
                options.add_argument("--headless")
        elif browser_name == "edge":
            options = EdgeOptions()
            if is_ci:
                options.add_argument("--headless")
        elif browser_name == "safari":
            options = SafariOptions()
            # Safari doesn't typically support headless in the same way
            # and might not need specific CI options for remote execution.
        else:
            raise ValueError(f"Unsupported browser for remote execution: {browser_name}")

        # Common capabilities/options setup for remote driver can go here if needed
        # For Selenium 4, desired_capabilities is deprecated for Remote. Options object is preferred.
        driver = webdriver.Remote(command_executor=remote_url, options=options)
    else:
        # Existing local driver logic
        if browser_name == "chrome":
            options = ChromeOptions()
            if is_ci:
                options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")
            driver = webdriver.Chrome(options=options)
        elif browser_name == "firefox":
            options = FirefoxOptions()
            if is_ci:
                options.add_argument("--headless")
            driver = webdriver.Firefox(options=options)
        elif browser_name == "edge":
            options = EdgeOptions()
            if is_ci:
                options.add_argument("--headless")
            driver = webdriver.Edge(options=options)
        elif browser_name == "safari":
            driver = webdriver.Safari()
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    try:
        driver.quit()
    except Exception as e:
        print(f"Error closing browser: {e}")