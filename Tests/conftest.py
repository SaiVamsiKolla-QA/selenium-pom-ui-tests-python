import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from Utility.utility import Utility

def pytest_addoption(parser):
    """
      Pytest hook that adds custom command-line options
      This allows us to specify which browser to use when running tests
    """
    parser.addoption("--browser", default="chrome",
                     help="Browser to run tests: chrome, firefox, edge, safari")

@pytest.fixture(scope="session")
def browser_name(request):
    """
        Session-scoped fixture that retrieves the browser name from command line arguments.
        The 'session' scope means this value is calculated once per test session.
    """
    return request.config.getoption("--browser").lower()

@pytest.fixture
def base_url():
    return "https://www.saucedemo.com/"

@pytest.fixture(scope='function')
def driver(browser_name):
    """Initialize and configure the WebDriver based on browser selection"""

    # Detect if running in CI environment
    is_ci = os.environ.get('CI') == 'true' or os.environ.get('GITHUB_ACTIONS') == 'true'

    # Chrome browser configuration
    if browser_name == "chrome":
        options = ChromeOptions()
        if is_ci:
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=options)
    # Firefox browser configuration
    elif browser_name == "firefox":
        options = FirefoxOptions()
        if is_ci:
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
    # Microsoft Edge browser configuration
    elif browser_name == "edge":
        options = EdgeOptions()
        if is_ci:
            options.add_argument("--headless")
        driver = webdriver.Edge(options=options)
    # Safari browser configuration
    elif browser_name == "safari":
        options = SafariOptions()
        if is_ci:
            options.add_argument("--headless")
        driver = webdriver.Safari()
    # Handle unsupported browser requests
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")


    # Create driver
    driver.maximize_window()
    driver.implicitly_wait(10)

    yield driver

    # Cleanup
    try:
        driver.quit()
    except Exception as e:
        print(f"Error closing browser: {e}")