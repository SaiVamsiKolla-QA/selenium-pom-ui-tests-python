import os
import json
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

def pytest_configure(config):
    """
    Pytest hook to configure test execution.
    Sets up Allure environment information.
    """
    allure_dir = config.getoption('--alluredir')
    if allure_dir:
        # Create environment.properties
        env_file = os.path.join(allure_dir, 'environment.properties')
        with open(env_file, 'w') as f:
            f.write(f"Browser={config.getoption('--browser')}\n")
            f.write(f"Remote URL={config.getoption('--remote-url') or 'local'}\n")
            f.write(f"Python Version={os.environ.get('PYTHON_VERSION', 'unknown')}\n")
            f.write(f"Environment=CI/CD\n")

        # Create categories.json
        categories = [
            {
                "name": "Test Failures",
                "matchedStatuses": ["failed"]
            },
            {
                "name": "Test Errors",
                "matchedStatuses": ["broken"]
            },
            {
                "name": "Test Skipped",
                "matchedStatuses": ["skipped"]
            },
            {
                "name": "Test Passed",
                "matchedStatuses": ["passed"]
            }
        ]
        
        categories_file = os.path.join(allure_dir, 'categories.json')
        with open(categories_file, 'w') as f:
            json.dump(categories, f, indent=2)

def pytest_addoption(parser):
    """Add command-line options for browser selection and remote execution"""
    parser.addoption("--browser", default="chrome",
                     help="Browser to run tests: chrome, firefox")
    parser.addoption("--remote-url", default=None,
                     help="Remote Selenium Grid URL (e.g., http://localhost:4444/wd/hub)")

@pytest.fixture(scope="session")
def browser_name(request):
    """Get browser name from command line"""
    return request.config.getoption("--browser").lower()

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
    """Return the base URL for tests"""
    return "https://www.saucedemo.com/"

def get_browser_options(browser_name, is_ci=False):
    """Configure browser options for local or CI execution"""
    if browser_name == "chrome":
        options = ChromeOptions()
        if is_ci:
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-infobars")
            options.add_argument("--remote-debugging-port=9222")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-setuid-sandbox")
    else:  # firefox
        options = FirefoxOptions()
        if is_ci:
            options.add_argument("--headless")
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
    
    return options

@pytest.fixture
def driver(browser_name, request):
    """Initialize WebDriver for test execution"""
    remote_url = request.config.getoption("--remote-url")
    is_ci = os.environ.get('CI') == 'true'
    driver = None
    
    try:
        options = get_browser_options(browser_name, is_ci)
        
        if remote_url:
            # Configure remote execution with detailed capabilities
            capabilities = {
                "browserName": browser_name,
                "platformName": "Linux",
                "se:name": "UI Automation Test",
                "se:vncEnabled": True,
            }
            
            if browser_name == "chrome":
                capabilities.update({
                    "goog:chromeOptions": {
                        "args": options.arguments,
                        "excludeSwitches": ["enable-automation"],
                        "extensions": [],
                        "prefs": {
                            "profile.default_content_settings.popups": 0,
                            "download.default_directory": "/tmp/downloads"
                        }
                    }
                })
            else:  # firefox
                capabilities.update({
                    "moz:firefoxOptions": {
                        "args": options.arguments,
                        "prefs": {
                            "browser.download.folderList": 2,
                            "browser.download.dir": "/tmp/downloads",
                            "browser.download.useDownloadDir": True
                        }
                    }
                })
            
            max_retries = 3
            retry_delay = 5
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    print(f"Attempt {attempt + 1} to create WebDriver session...")
                    driver = webdriver.Remote(
                        command_executor=remote_url,
                        options=options
                    )
                    driver.set_window_size(1920, 1080)
                    driver.implicitly_wait(10)
                    print("WebDriver session created successfully!")
                    break
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        print(f"Attempt {attempt + 1} failed: {str(e)}")
                        print(f"Retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)
                    else:
                        print(f"All {max_retries} attempts failed. Last error: {str(e)}")
                        raise
        else:
            # Configure local execution
            if browser_name == "chrome":
                driver = webdriver.Chrome(options=options)
            else:
                driver = webdriver.Firefox(options=options)
            
            driver.maximize_window()
            driver.implicitly_wait(10)
        
        yield driver
        
    except Exception as e:
        print(f"Error setting up WebDriver: {str(e)}")
        raise
    
    finally:
        if driver:
            try:
                if request.node.rep_call.failed:
                    allure.attach(
                        driver.get_screenshot_as_png(),
                        name="Failure Screenshot",
                        attachment_type=allure.attachment_type.PNG
                    )
            except: pass
            driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store test result for screenshot capture on failure"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)