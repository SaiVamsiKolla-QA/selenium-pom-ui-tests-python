# Swag Labs Automation Framework

A Page Object Model based Selenium automation framework for testing the Swag Labs demo website. This framework includes
end-to-end test scenarios from login to checkout with Allure reporting integration.

## Features

- Page Object Model design pattern
- Cross-platform compatibility (Windows and Mac)
- Allure reporting with screenshots at each test step
- Randomized product selection for testing
- Comprehensive test coverage from login to checkout

## Prerequisites

- Python 3.9 or higher
- Chrome browser
- Java JDK 8 or higher (required for Allure reporting)

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/VamsiKolla-QA/SWAG-POM_V.git
   cd SWAG-POM_V
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # Mac/Linux
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r Requirements.txt
   ```

4. Install Allure:
    - Windows (using Scoop):
      ```
      scoop install allure
      ```
    - Windows (using Chocolatey):
      ```
      choco install allure-commandline
      ```
    - Mac:
      ```
      brew install allure
      ```

## Project Structure

```
SWAG-POM_V/
├── Pages/                  # Page Object classes
├── Utility/                # Helper functions and utilities
├── tests/                  # Test scripts
├── assets/                 # Screenshots and other assets
│   └── screenshots/        # Test execution screenshots
├── allure-results/         # Allure test results
├── run_tests.bat           # Windows test execution script
├── run_tests.sh            # Mac/Linux test execution script
└── Requirements.txt        # Project dependencies
└── TestCases-SwagLabs.xlsx # Functional Test Scenarios  
```

## Running Tests

### Using Scripts

Run all tests with Allure reporting:

- Windows:
  ```
  run_tests.bat
  ```

- Mac/Linux:
  ```
  ./run_tests.sh
  ```

### Manual Execution

Run specific tests:

```bash
# Run a specific test file
pytest tests/test_login.py -v --alluredir=allure-results

# Run a specific test
pytest tests/test_checkout_overview.py::test_swag_checkout_overview -v --alluredir=allure-results

# Generate Allure report
allure serve allure-results
```

## Test Scenarios

1. **Login Test**
    - Validates user login functionality

2. **Products Test**
    - Adds random products to cart
    - Verifies cart count

3. **Cart Test**
    - Adds products to cart
    - Navigates to cart
    - Proceeds to checkout

4. **Checkout Information Test**
    - Completes user information form
    - Verifies entered information
    - Navigates to overview page

5. **Checkout Overview Test**
    - Complete end-to-end checkout process
    - Finishes order

## Troubleshooting

### Common Issues

1. **WebDriver issues**
    - The framework uses webdriver-manager to automatically download the correct ChromeDriver version. If you encounter
      issues, try updating Chrome browser.

2. **Allure Report Not Generating**
    - Ensure Java is installed and configured properly
    - Verify allure-pytest package is installed
    - Run `allure --version` to check if Allure is properly installed

3. **Test Failures**
    - Check the screenshots in the assets/screenshots directory
    - Review the Allure report for detailed step information

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.