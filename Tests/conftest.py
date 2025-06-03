import os
import allure # Make sure allure is imported
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


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

def get_browser_options(browser_name, is_ci=False):
    """Helper function to get browser-specific options"""
    options = None
    if browser_name == "chrome":
        options = ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        if is_ci:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
    elif browser_name == "firefox":
        options = FirefoxOptions()
        if is_ci:
            options.add_argument("--headless")
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
    elif browser_name == "edge":
        options = EdgeOptions()
        if is_ci:
            options.add_argument("--headless")
    elif browser_name == "safari":
        options = SafariOptions()
    
    return options

@pytest.fixture(scope='function')
def driver(browser_name, request):
    """Initialize WebDriver with enhanced remote execution support"""
    remote_url = request.config.getoption("--remote-url")
    is_ci = os.environ.get('CI') == 'true' or os.environ.get('GITHUB_ACTIONS') == 'true'
    
    try:
        options = get_browser_options(browser_name, is_ci)
        
        if not options:
            raise ValueError(f"Unsupported browser: {browser_name}")

        if remote_url:
            # Set common capabilities for remote execution
            options.set_capability("platformName", "Linux")
            options.set_capability("browserName", browser_name)
            options.set_capability("se:name", f"UI Test - {browser_name}")
            
            # Add browser-specific capabilities
            if browser_name == "chrome":
                chrome_prefs = {}
                chrome_prefs["profile.default_content_settings"] = {"images": 2}
                chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
                options.add_experimental_option("prefs", chrome_prefs)
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")
                options.add_argument("--disable-extensions")
                options.add_argument("--proxy-server='direct://'")
                options.add_argument("--proxy-bypass-list=*")
                options.add_argument("--start-maximized")
                options.add_argument("--headless=new")
            elif browser_name == "firefox":
                options.add_argument("--headless")
                options.add_argument("--width=1920")
                options.add_argument("--height=1080")
                options.set_preference("browser.download.folderList", 2)
                options.set_preference("browser.download.manager.showWhenStarting", False)
                options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-debian-package")
            
            # Add logging preferences
            options.set_capability("se:recordVideo", True)
            
            with allure.step(f"Creating remote driver for {browser_name} at {remote_url}"):
                driver = webdriver.Remote(
                    command_executor=remote_url,
                    options=options
                )
        else:
            with allure.step(f"Creating local driver for {browser_name}"):
                if browser_name == "chrome":
                    driver = webdriver.Chrome(options=options)
                elif browser_name == "firefox":
                    driver = webdriver.Firefox(options=options)
                elif browser_name == "edge":
                    driver = webdriver.Edge(options=options)
                elif browser_name == "safari":
                    driver = webdriver.Safari(options=options)
        
        # Common setup
        driver.maximize_window()
        driver.implicitly_wait(10)
        
        # Add driver information to Allure report
        allure.attach(
            str(driver.capabilities),
            name="Driver Capabilities",
            attachment_type=allure.attachment_type.JSON
        )
        
        yield driver
        
    except Exception as e:
        allure.attach(
            str(e),
            name="Driver Setup Error",
            attachment_type=allure.attachment_type.TEXT
        )
        raise
    
    finally:
        try:
            if 'driver' in locals():
                driver.quit()
        except Exception as e:
            print(f"Error closing browser: {e}")