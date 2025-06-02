# 🚀 Selenium POM UI Automation Framework

[![Selenium Grid CI](https://github.com/SaiVamsiKolla-QA/selenium-pom-ui-tests-python/actions/workflows/selenium-grid-ci.yml/badge.svg)](https://github.com/SaiVamsiKolla-QA/selenium-pom-ui-tests-python/actions/workflows/selenium-grid-ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.10-blue)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/selenium-4.18.1-green)](https://selenium-python.readthedocs.io/)
[![Pytest](https://img.shields.io/badge/pytest-7.x-orange)](https://docs.pytest.org/)
[![Allure](https://img.shields.io/badge/allure-2.27.0-yellow)](https://docs.qameta.io/allure/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[**📊 Latest Allure Report**](https://saivamsikolla-qa.github.io/selenium-pom-ui-tests-python/) | [**🔗 Swag Labs Demo**](https://www.saucedemo.com/)

A robust, production-ready Selenium automation framework built with Python and pytest, implementing the Page Object Model (POM) design pattern. Features comprehensive CI/CD integration, Selenium Grid support, and detailed Allure reporting with historical trends.
---

## ✨ Key Features

### Core Capabilities
- **🏗️ Page Object Model (POM)** - Clean, maintainable test architecture
- **🌐 Cross-Browser Support** - Chrome, Firefox, Edge, Safari
- **⚡ Parallel Execution** - Multi-threaded test execution with configurable workers
- **🔄 Cross-Browser Parallel** - Run tests simultaneously across multiple browsers
- **🎯 Flexible Parallelization** - Browser-level and test-level parallel execution
- **🖥️ Cross-Platform** - Windows, macOS, Linux compatibility
- **📸 Visual Documentation** - Automatic screenshot capture at every step

### Advanced Features
- **📊 Allure Reporting** - Rich reports with history trends and analytics
- **🔄 CI/CD Integration** - GitHub Actions with automated deployments
- **📈 Performance Metrics** - Execution statistics and trend analysis
- **📧 Email Notifications** - Automated test result summaries
- **🎯 Flexible Execution** - Multiple test execution strategies
- **🧹 Auto-Cleanup** - Browser process management
---
## 📋 Prerequisites

Before running the tests, ensure you have the following installed:

| Software | Version | Purpose | Installation Guide |
|----------|---------|---------|-------------------|
| Python | 3.10+ | Core runtime | [python.org](https://www.python.org/downloads/) |
| Docker Desktop | Latest | Selenium Grid & containers | [docker.com](https://www.docker.com/products/docker-desktop/) |
| Java | 8+ | Allure reporting | [oracle.com/java](https://www.oracle.com/java/technologies/downloads/) |
---
## 📁 Project Structure

```
selenium-pom-ui-tests-python/
├── 📂 .github/
│   └── workflows/
│       └── selenium-grid-ci.yml    # GitHub Actions CI/CD workflow
├── 📂 Pages/                       # Page Object Model classes
│   ├── login_page.py              # Login page objects
│   ├── inventory_page.py          # Product listing page
│   └── checkout_page.py           # Checkout flow pages
├── 📂 Tests/                       # Test scripts
│   ├── conftest.py                # Pytest fixtures & configuration
│   ├── test_swag_login.py         # Login functionality tests
│   └── assets/                    # Test-specific assets
├── 📂 Utility/                     # Helper functions
│   └── utility.py                 # Common utilities
├── 📂 allure-results/             # Test results directory
│   ├── environment.properties     # Environment configuration
│   └── categories.json           # Test categorization rules
├── 📂 allure-report/              # Generated HTML reports
├── 📂 reports/                    # Archived test reports
├── 📂 .pytest_cache/              # Pytest cache directory
├── 📄 pytest.ini                  # Pytest configuration
├── 📄 Dockerfile                  # Container configuration
├── 📄 docker-compose.yml          # Selenium Grid orchestration
├── 📄 requirements.txt            # Python dependencies
├── 📄 setup_check.py             # Environment verification
├── 📄 cleanup.py                 # Browser process cleanup
└── 📄 README.md                   # Project documentation
```

### Browser Support
- Chrome (default)
- Firefox
- Edge
- Safari (local only)
---
## 🚀 Quick Start

1. **Clone Repository**
   ```bash
   git clone https://github.com/SaiVamsiKolla-QA/selenium-pom-ui-tests-python.git
   cd selenium-pom-ui-tests-python
   ```

2. **Set Up Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

3. **Run Tests**
   ```bash
   # Run all tests
   pytest

   # Run specific test category
   pytest -m smoke
   pytest -m "smoke and not login"

   # Run with specific browser
   pytest --browser chrome
   pytest --browser firefox
   ```

4. **Run with Selenium Grid**
   ```bash
   # Start Selenium Grid
   docker-compose up -d

   # Run tests against Grid
   pytest --remote-url http://localhost:4444/wd/hub
   ```

5. **Parallel Cross-Browser Testing**
   ```bash
   # Run the parallel cross-browser test script
   ./run_parallel_cross_browser.sh

   # Available options:
   #  -w, --workers N        Number of parallel workers (default: 4)
   #  -b, --browsers LIST    Comma-separated list of browsers (default: chrome,firefox)
   #  -u, --url URL         Remote Selenium Grid URL (default: http://localhost:4444/wd/hub)
   #  -t, --tests PATH      Test path (default: Tests/)

   # Examples:
   # Run with 6 workers on all browsers
   ./run_parallel_cross_browser.sh -w 6 -b chrome,firefox,edge

   # Run specific tests with 4 workers
   ./run_parallel_cross_browser.sh -t Tests/test_swag_login.py

   # Run on custom Selenium Grid
   ./run_parallel_cross_browser.sh -u http://custom-grid:4444/wd/hub

   # Combined options
   ./run_parallel_cross_browser.sh -w 6 -b chrome,firefox -t Tests/test_swag_login.py -u http://localhost:4444/wd/hub
   ```

## 📊 Test Reports

### Local Execution
```bash
# Generate Allure report
allure generate allure-results -o allure-report --clean

# Open report
allure open allure-report
```

### CI/CD Pipeline
- Automated report generation
- GitHub Pages deployment
- Email notifications with test results
- Historical trend analysis

## 🔧 Environment Configuration

### Supported Browsers
- Chrome (default)
- Firefox
- Edge
- Safari (local only)


## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Selenium](https://www.selenium.dev/)
- [Pytest](https://docs.pytest.org/)
- [Allure Framework](https://docs.qameta.io/allure/)
- [Sauce Demo](https://www.saucedemo.com/)