# 🚀 POM UI Automation Framework

[![CI with Dynamic Allure Report and Email](https://github.com/SaiVamsiKolla-QA/selenium-pom-ui-tests-python/actions/workflows/selenium-tests.yml/badge.svg)](https://github.com/SaiVamsiKolla-QA/selenium-pom-ui-tests-python/actions/workflows/selenium-tests.yml)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/selenium-4.x-green)](https://selenium-python.readthedocs.io/)
[![Pytest](https://img.shields.io/badge/pytest-7.x-orange)](https://docs.pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[**📊 Latest Allure Report**](https://saivamsikolla-qa.github.io/selenium-pom-ui-tests-python/) | [**🔗 Swag Labs demo website**](https://www.saucedemo.com/)

A robust Selenium automation framework built with Python and pytest, implementing the Page Object Model (POM) design pattern. Features comprehensive CI/CD integration with GitHub Actions and detailed Allure reporting.

---

## ✨ Features

- **🏗️ Page Object Model (POM)** - Clean, maintainable test architecture
- **🌐 Cross-Browser Support** - Chrome, Firefox, Edge, Safari
- **⚡ Parallel Test Execution** - Faster test runs with pytest-xdist
- **🖥️ Cross-Platform** - Windows, macOS, Linux compatibility
- **📸 Visual Documentation** - Screenshots captured at every test step
- **📊 Comprehensive Reporting** - Detailed Allure reports with analytics
- **🔄 CI/CD Integration** - Automated testing with GitHub Actions
- **📈 Test Statistics** - Multi-run execution with performance metrics
- **📧 Email Notifications** - Automated test result notifications

---

## 🛠️ Prerequisites

Before getting started, ensure you have the following installed:

| Requirement | Version | Purpose |
|-------------|---------|---------|
| **Python** | 3.9+ | Core runtime |
| **Git** | Latest | Version control |
| **Google Chrome** | Latest | Default browser for testing |
| **Java JDK** | 8+ | Required for Allure reporting |

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/SaiVamsiKolla-QA/selenium-pom-ui-tests-python.git
cd selenium-pom-ui-tests-python
```

### 2. Set Up Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r Requirements.txt
```

### 4. Verify Installation

```bash
python setup_check.py
```

This script validates:
- ✅ Python version compatibility
- ✅ Required packages installation
- ✅ Browser availability
- ✅ Allure CLI setup

---

## 🔧 Allure Setup

Allure is required for generating detailed test reports.

### macOS (Homebrew)
```bash
brew install allure
```

### Windows (Scoop)
```bash
scoop install allure
```

### Windows (Chocolatey)
```bash
choco install allure-commandline
```

### Verify Installation
```bash
allure --version
```

---

## 📁 Project Structure

```
selenium-pom-ui-tests-python/
├── 📂 .github/
│   └── workflows/              # GitHub Actions CI/CD workflows
├── 📂 Pages/                   # Page Object Model classes
├── 📂 Utility/                 # Helper functions and utilities
├── 📂 Tests/                   # Test scripts and test cases
├── 📂 assets/
│   └── screenshots/            # Test execution screenshots
├── 📂 allure-results/          # Allure test results
├── 📂 reports/                 # Generated test reports
├── 📄 setup_check.py           # Environment verification script
├── 📄 multiple_tests.py        # Multi-run test execution script
├── 📄 run_tests.sh             # Test execution shell script
├── 📄 Requirements.txt         # Python dependencies
├── 📄 Testcases-SwagLabs.xlsx  # Manual test scenarios
└── 📄 README.md               # Project documentation
```

---

## 🏃‍♂️ Running Tests

### Quick Test Execution

**Windows:**
```bash
run_tests.bat
```

**macOS/Linux:**
```bash
./run_tests.sh
```

### Manual Test Execution

#### Run Specific Tests
```bash
# Single test file
python -m pytest Tests/test_swag_login.py -v --alluredir=allure-results

# Specific test method
pytest Tests/test_swag_end_to_end.py::test_swag_end_to_end -v --alluredir=allure-results
```

#### Parallel Execution
```bash
# Run with 6 parallel workers
python -m pytest Tests/test_swag_login.py -n 6 --alluredir=allure-results
```

#### Generate Allure Report
```bash
allure serve allure-results
```

---

## 🌐 Cross-Browser Testing

The framework supports testing across multiple browsers with easy configuration.

### Supported Browsers

| Browser | Command Flag | Notes |
|---------|--------------|-------|
| Chrome | `--browser chrome` (default) | Auto-managed WebDriver |
| Firefox | `--browser firefox` | Requires Firefox installation |
| Edge | `--browser edge` | Requires Microsoft Edge |
| Safari | `--browser safari` | macOS only, manual setup required |

### Browser-Specific Execution

```bash
# Chrome (default)
python -m pytest Tests/test_swag_login.py -v --alluredir=allure-results/chrome

# Firefox
python -m pytest Tests/test_swag_login.py -v --browser firefox --alluredir=allure-results/firefox

# Edge
python -m pytest Tests/test_swag_login.py -v --browser edge --alluredir=allure-results/edge

# Safari (macOS only)
python -m pytest Tests/test_swag_login.py -v --browser safari --alluredir=allure-results/safari

# Firefox with parallel execution
python -m pytest Tests/test_swag_login.py -n 4 --browser firefox --alluredir=allure-results/firefox
```

### Safari Setup (macOS)

1. Open Safari
2. Go to **Develop** menu
3. Enable **"Allow Remote Automation"**

*Note: Safari doesn't support parallel testing*

---

## 📊 Multi-Run Statistics

Execute tests multiple times to gather performance statistics and reliability metrics.

### Basic Multi-Run
```bash
python multiple_tests.py Tests/test_swag_checkout_step_one.py::test_swag_checkout_step_one -n 10
```

### Advanced Multi-Run with Browser Selection
```bash
# Firefox tests with 6 parallel workers, 10 iterations
python run_tests.py Tests/test_swag_login.py -n 10 --browser firefox --parallel 6
```

### Generated Metrics
- 📈 **Success Rate** - Percentage of passed tests
- ⏱️ **Execution Times** - Average, minimum, maximum
- 📝 **Detailed Logs** - Complete execution history

---

## 🔄 Continuous Integration

### GitHub Actions Workflow

The project includes a comprehensive CI/CD pipeline that:

- 🔄 **Triggers** on push/pull requests to main branch
- 🐍 **Sets up** Python environment and dependencies
- 🌐 **Installs** Chrome browser and WebDriver
- 📊 **Configures** Allure reporting CLI
- 🧪 **Executes** complete test suite
- 📈 **Generates** detailed Allure reports
- 🚀 **Deploys** reports to GitHub Pages
- 📧 **Sends** email notifications with results

### Manual Workflow Trigger

1. Navigate to the **Actions** tab in your repository
2. Select **"CI with Dynamic Allure Report and Email"**
3. Click **"Run workflow"** dropdown
4. Choose the branch and parameters
5. Click **"Run workflow"**

### View Results

- 📊 **Live Reports**: [GitHub Pages](https://saivamsikolla-qa.github.io/selenium-pom-ui-tests-python/)
- 🔍 **Workflow Logs**: Repository Actions tab
- 📧 **Email Summary**: Automated notifications

---

## 🧪 Test Coverage

### Current Test Scenarios

| Test Suite | Description | Status |
|------------|-------------|--------|
| **Login Tests** | Valid/invalid credential verification | ✅ |
| **End-to-End** | Complete user journey testing | ✅ |
| **Checkout Process** | Multi-step checkout validation | ✅ |
| **Cross-Browser** | Browser compatibility testing | ✅ |

### Sample Test Execution

The framework validates login functionality with various user types:
- Standard users
- Problem users  
- Performance glitch users
- Error users

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### WebDriver Problems
```bash
# Issue: ChromeDriver version mismatch
# Solution: Update Chrome browser
# The webdriver-manager automatically handles driver downloads
```

#### Allure Report Generation
```bash
# Issue: Allure reports not generating
# Check: Java installation
java --version

# Check: Allure CLI installation
allure --version

# Verify: allure-pytest package
pip show allure-pytest
```

#### Test Failures
1. **Screenshots**: Check `assets/screenshots/` for visual debugging
2. **Logs**: Review detailed logs in Allure reports
3. **Stack Traces**: Full error details available in Allure report

#### Python Environment
```bash
# Issue: Import errors
# Solution: Verify virtual environment activation
which python  # Should point to .venv directory

# Reinstall dependencies if needed
pip install -r Requirements.txt --force-reinstall
```

### Getting Help

If you encounter issues:
1. 📸 Check screenshots in `assets/screenshots/`
2. 📊 Review the Allure report for stack traces
3. 🔍 Verify environment with `python setup_check.py`
4. 📝 Create an issue with error details

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Setup

1. **Fork** the repository
2. **Clone** your fork locally
3. **Create** a feature branch
   ```bash
   git checkout -b feature/amazing-feature
   ```
4. **Make** your changes
5. **Test** your changes thoroughly
6. **Commit** with clear messages
   ```bash
   git commit -m "Add amazing feature"
   ```
7. **Submit** a pull request

### Contribution Guidelines

- ✅ Follow PEP 8 style guidelines
- ✅ Add tests for new features
- ✅ Update documentation as needed
- ✅ Ensure all tests pass
- ✅ Include clear commit messages

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- [Selenium WebDriver](https://selenium-python.readthedocs.io/) for browser automation
- [Pytest](https://docs.pytest.org/) for testing framework
- [Allure Framework](https://docs.qameta.io/allure/) for reporting
- [Swag Labs](https://www.saucedemo.com/) for providing the demo application

---

## 📞 Support

- 📧 **Email**: [saivamsikolla@gmail.com]
- 🐛 **Issues**: [GitHub Issues](https://github.com/SaiVamsiKolla-QA/selenium-pom-ui-tests-python/issues)
- 📚 **Wiki**: [Project Wiki](https://github.com/SaiVamsiKolla-QA/selenium-pom-ui-tests-python/wiki)

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ by [Your Name]

</div>
