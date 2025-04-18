import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def base_url():
    return "https://www.saucedemo.com/"

@pytest.fixture(scope='function')
def driver():
    """Initialize and configure the Chrome WebDriver for both local and CI environments."""
    # Detect if running in CI environment
    is_ci = os.environ.get('CI') == 'true' or os.environ.get('GITHUB_ACTIONS') == 'true'

    chrome_options = Options()

    # For CI environment, use headless mode
    if is_ci:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

    # Create driver (without webdriver-manager)
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)

    yield driver

    # Cleanup
    try:
        driver.quit()
    except:
        pass