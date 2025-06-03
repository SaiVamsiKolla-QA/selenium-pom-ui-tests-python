class BasePage:
    """Base class for all page objects"""

    def __init__(self, driver):
        self.driver = driver
        self.default_timeout = 10

    def open_url(self, url):
        """Open a URL in the browser"""
        self.driver.get(url)

