class BasePage:
    """
    Base class for all page objects with common utilities and methods.
    This class implements common functionality that will be reused across different pages.
    """

    def __init__(self, driver):
        """
        Initialize the base page with a WebDriver instance.

        """
        self.driver = driver
        self.default_timeout = 10

    def open_url(self, url):
        """
        Open a specific URL in the browser.
        """
        self.driver.get(url)

