#  POM UI Automation Framework

This is a Selenium automation framework developed in Python using pytest. Based on the Page Object Model, it automates end-to-end test scenarios for 
the [Swag Labs demo website](https://www.saucedemo.com/). from login through checkout and integrates Allure for detailed reporting.

---

## Features

- Page Object Model (POM) design pattern
- Cross-platform support (Windows, Mac, Linux)
- Allure reports with screenshots at every test step
- Support Parallel Testing
- Support Cross Browser Testing 
- Multi-run test execution with statistics
- GitHub Actions CI/CD integration

---

## Prerequisites

- Python 3.9 or higher
- Git
- Google Chrome
- Java JDK 8 or higher *(required for Allure reporting)*

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/VamsiKolla-QA/SwagLabs-POM-E2E.git
cd Python-Selenium-POM
```

### 2. Create and activate the virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r Requirements.txt
```

---

## Environment Check

Before installing additional tools like Allure, verify your setup:

```bash
python setup_check.py
```

This script checks for:

- Python version (>= 3.9)
- Required pip packages
- Chrome browser
- Allure CLI availability

If something is missing, it will guide you to fix it.

---

## Install Allure (if needed)

### Mac:

```bash
brew install allure
```

### Windows (Scoop):

```bash
scoop install allure
```

### Windows (Chocolatey):

```bash
choco install allure-commandline
```

---

## Project Structure

```
Python-Selenium-POM/
├── .github/
│   └── workflows/          # GitHub Actions workflow files
├── Pages/                  # Page Object classes
├── Utility/                # Helper functions and utilities
├── Tests/                  # Test scripts
├── assets/
│   └── screenshots/        # Screenshots from test runs
├── allure-results/         # Allure results directory
├── reports/                # Generated test reports
├── setup_check.py          # Environment verification script
├── multiple_tests.py       # Python script for repeated test execution with statistics
├── run_tests.sh            # Shell script for running tests
├── Requirements.txt        # Python dependencies
└── Testcases-SwagLabs.xlsx # Manual test scenarios
```

---

## Running Tests

### Using Scripts

Run all tests with Allure reporting:

**Windows:**

```bash
run_tests.bat
```

**Mac/Linux:**

```bash
./run_tests.sh
```

### Manual Execution

Run a specific test file:

```bash
python -m pytest Tests/test_swag_login.py -v --alluredir=allure-results
```
Run a parallel test :
````
python -m pytest Tests/test_swag_login.py -n 6 --alluredir=allure-results
````
End-to-End Checkout Test:

```bash
pytest Tests/test_swag_end_to_end.py::test_swag_end_to_end -v --alluredir=allure-results 
```

Generate and view Allure Report:

```bash
allure serve allure-results
```
## Parallel Test Execution

This framework supports parallel test execution using pytest-xdist, significantly reducing execution time.

Run with 6 parallel workers
```bash
python -m pytest Tests/test_swag_login.py -n 6 --alluredir=allure-results
```

## Cross-Browser Testing

This framework supports automated testing across multiple browsers:

- Chrome (default)
- Firefox
- Edge
- Safari (macOS only)

### Running Tests on Different Browsers


# Run with Chrome (default)
``` bash
python -m pytest Tests/test_swag_login.py -v --alluredir=allure-results/chrome
```
# Run with Firefox
``` bash
python -m pytest Tests/test_swag_login.py -v --browser firefox --alluredir=allure-results/firefox
```
# Run with Edge
``` bash
python -m pytest Tests/test_swag_login.py -v --browser edge --alluredir=allure-results/edge
```
# Run with Safari (macOS only)
``` bash
python -m pytest Tests/test_swag_login.py -v --browser safari --alluredir=allure-results/safari
```
# Run with specific browser in parallel
``` bash
python -m pytest Tests/test_swag_login.py -n 4 --browser firefox --alluredir=allure-results/firefox
```

Browser-Specific Notes

- Safari: Requires enabling "Allow Remote Automation" in Safari's Develop menu and it don't support parallel testing
- Edge: Requires Microsoft Edge to be installed
- Firefox: Requires Firefox to be installed
- Chrome: Default browser, used if no browser is specified

### Using Multi-Run Script
Run a specific test multiple times and collect statistics:
```bash
python multiple_tests.py Tests/test_swag_checkout_step_one.py::test_swag_checkout_step_one -n 10
```
Run a specific test multiple times in parallel on specific  browser and collect statistics:
```bash
# Run Firefox tests with 6 parallel workers, 10 iterations
python run_tests.py Tests/test_swag_login.py -n 10 --browser firefox --parallel 6
```

This will:

- Run the specified test 10 times
- Log all test executions
- Calculate success rate
- Measure average, min, and max execution times

## Continuous Integration
This project uses GitHub Actions for continuous integration. Every push and pull request to the main branch triggers the following workflow:

- Setup of Python and dependencies
- Installation of Chrome browser
- Installation of Allure Report CLI
- Execution of all tests:
- Generation of Allure Report
- Artifact uploading (report and screenshots)

You can view the test results in the Actions tab of the GitHub repository.
To run the GitHub Actions workflow manually:

- Go to the Actions tab in your repository
- Select "Swag Labs E2E Tests" workflow
- Click "Run workflow"



### Login Test

- Verifies login with valid credentials for various user types.





---

## Troubleshooting

### WebDriver Issues

- Make sure Chrome is up-to-date
- `webdriver-manager` auto-downloads correct ChromeDriver

### Allure Report Not Generating

- Ensure Java is installed and added to the system path
- Verify `allure-pytest` is installed
- Confirm `allure --version` works

### Test Failures

- Check screenshots in `assets/screenshots`
- Review the Allure report for full stack trace

---

## 🌐 Contributing

1. Fork the repo
2. Create a feature branch
3. Make changes
4. Submit a pull request

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).

