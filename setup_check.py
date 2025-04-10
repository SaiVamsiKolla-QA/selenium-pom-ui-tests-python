# setup_check.py
import subprocess
import sys
import platform
import pkg_resources
import os


def check_python_version():
    """Check if Python version is compatible."""
    major, minor = sys.version_info[:2]
    if major < 3 or (major == 3 and minor < 9):
        print(f"❌ Python 3.9 or higher required. You have {major}.{minor}")
        return False
    print(f"✅ Python version: {major}.{minor}")
    return True


def check_packages():
    """Check if all required packages are installed."""
    try:
        requirements_path = "requirements.txt"
        if not os.path.exists(requirements_path):
            print("❌ requirements.txt not found")
            return False

        with open(requirements_path) as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

        pkg_resources.require(requirements)
        print("✅ All Python packages are installed")
        return True
    except pkg_resources.DistributionNotFound as e:
        print(f"❌ Missing package: {e}")
        print("Run: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Error checking packages: {e}")
        return False


def check_allure():
    """Check if Allure is installed."""
    try:
        result = subprocess.run(["allure", "--version"], check=True, capture_output=True, text=True)
        version = result.stdout.strip()
        print(f"✅ Allure is installed: {version}")
        return True
    except FileNotFoundError:
        print("❌ Allure command-line tool is not installed")
        os_type = platform.system()
        if os_type == "Windows":
            print("\nWindows installation options:")
            print("Option 1: scoop install allure")
            print("Option 2: choco install allure-commandline")
        elif os_type == "Darwin":
            print("\nMac installation option:")
            print("brew install allure")
        else:
            print("\nLinux installation option:")
            print("sudo apt-add-repository ppa:qameta/allure")
            print("sudo apt-get update")
            print("sudo apt-get install allure")
        return False
    except Exception as e:
        print(f"❌ Error checking Allure: {e}")
        return False


def check_chrome():
    """Check if Chrome is installed."""
    try:
        if platform.system() == "Windows":
            process = subprocess.run(["where", "chrome"], check=True, capture_output=True, text=True)
        else:
            process = subprocess.run(["which", "google-chrome"], check=True, capture_output=True, text=True)
        print("✅ Chrome browser is installed")
        return True
    except:
        print("❌ Chrome browser not found")
        print("Please install Chrome browser")
        return False


def main():
    """Run all environment checks."""
    print("🔍 Checking environment for SwagLabs-POM-E2E...\n")

    python_ok = check_python_version()
    packages_ok = check_packages()
    allure_ok = check_allure()
    chrome_ok = check_chrome()

    print("\n📋 Environment Check Summary:")
    print(f"Python 3.9+: {'✅' if python_ok else '❌'}")
    print(f"Required packages: {'✅' if packages_ok else '❌'}")
    print(f"Allure: {'✅' if allure_ok else '❌'}")
    print(f"Chrome: {'✅' if chrome_ok else '❌'}")

    if all([python_ok, packages_ok, allure_ok, chrome_ok]):
        print("\n✅ All checks passed! Your environment is ready to run the tests.")
        return 0
    else:
        print("\n❌ Some checks failed. Please fix the issues listed above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())