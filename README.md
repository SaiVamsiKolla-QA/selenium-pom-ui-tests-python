# Swag Labs Automation Framework

A Page Object Model-based Selenium automation framework for testing
the [Swag Labs demo website](https://www.saucedemo.com/). It includes full end-to-end scenarios from login to checkout
with Allure reporting integration.

---

## Features

- Page Object Model (POM) design pattern
- Cross-platform support (Windows, Mac, Linux)
- Allure reports with screenshots at every test step
- Randomized product selection
- End-to-end test scenarios covering login through order finish
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
cd SwagLabs-POM-E2E
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

## Environment Check (Run First!)

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
SwagLabs-POM-E2E/
├── Pages/                  # Page Object classes
├── Utility/                # Helper functions and utilities
├── tests/                  # Test scripts
├── assets/
│   └── screenshots/        # Screenshots from test runs
├── allure-results/         # Allure results directory
├── setup_check.py          # Environment verification script
├── run_tests.sh            # Shell script for running tests (Mac/Linux)
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
pytest tests/test_login.py -v --alluredir=allure-results
```

End-to-End Checkout Test:

```bash
pytest tests/test_end_to_end.py::test_swag_checkout_end_to_end -v --alluredir=allure-results
```

Generate and view Allure Report:

```bash
allure serve allure-results
```

---

## 🚄 CI/CD Pipeline (GitHub Actions)

### Workflow Features:

- Auto-run tests on push to `main` or pull requests
- Cross-platform runner setup
- Chrome browser installation
- Allure report generation
- Artifacts available for download

### View Results:

1. Go to **Actions** tab in GitHub
2. Select the latest workflow run
3. Download the Allure report artifact

---

## 🔢 End-to-End Test Scenarios

### Login Test

- Verifies login with valid credentials

### Products Test

- Adds 2 random products to cart
- Verifies cart count matches

### Cart Test

- Navigates to cart page
- Proceeds to checkout

### Checkout Information Test

- Fills user details
- Verifies info submission

### Overview & Finish Test

- Reviews summary page
- Completes order

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
<<<<<<< HEAD

## 📝 License

This project is licensed under the [MIT License](LICENSE).

i need to copy it in PyCharm so can you give it that

=======

## 📝 License

This project is licensed under the [MIT License](LICENSE).

i need to copy it in PyCharm so can you give it that> > > > > > > fb78c11 (Local updates)
