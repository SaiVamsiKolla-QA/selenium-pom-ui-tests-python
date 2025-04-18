#!/usr/bin/env python3
"""
Comprehensive environment check for Python-Selenium-POM project
"""

import importlib.metadata
import os
import platform
import subprocess
import sys
from typing import Tuple, Dict, List

# Constants
REQUIREMENTS_FILE = "requirements.txt"
CHROME_MAC_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def print_header(title: str) -> None:
    """Print formatted section header"""
    print(f"\n\033[1m{title}\033[0m")
    print("-" * len(title))


def check_python_version() -> Tuple[bool, str]:
    """Check Python version compatibility"""
    required = (3, 9)
    current = sys.version_info[:2]
    version_str = f"{current[0]}.{current[1]}"

    if current >= required:
        return True, f"✅ Python {version_str} (meets minimum 3.9+)"
    return False, f"❌ Python {version_str} (requires 3.9+)"


def check_packages() -> Tuple[bool, List[str]]:
    """Check required Python packages"""
    if not os.path.exists(REQUIREMENTS_FILE):
        return False, ["requirements.txt not found"]

    with open(REQUIREMENTS_FILE) as f:
        requirements = [
            line.strip()
            for line in f
            if line.strip() and not line.startswith('#')
        ]

    missing = []
    for req in requirements:
        pkg = req.split('==')[0].split('>')[0].split('<')[0].strip()
        try:
            importlib.metadata.version(pkg)
        except importlib.metadata.PackageNotFoundError:
            missing.append(pkg)

    if not missing:
        return True, ["✅ All required packages installed"]
    return False, [f"❌ Missing package: {pkg}" for pkg in missing]


def check_allure() -> Tuple[bool, str]:
    """Check Allure CLI installation"""
    try:
        result = subprocess.run(
            ["allure", "--version"],
            check=True,
            capture_output=True,
            text=True,
            timeout=5
        )
        return True, f"✅ Allure {result.stdout.strip()}"
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return False, "❌ Allure not found (install via brew/choco/scoop)"


def check_chrome() -> Tuple[bool, str]:
    """Check Chrome browser installation with macOS support"""
    system = platform.system()

    if system == "Darwin":
        if os.path.exists(CHROME_MAC_PATH):
            try:
                version = subprocess.run(
                    [CHROME_MAC_PATH, "--version"],
                    capture_output=True,
                    text=True
                )
                return True, f"✅ Chrome {version.stdout.strip().replace('Google Chrome ', '')}"
            except:
                return True, "✅ Chrome found (version check failed)"
        return False, "❌ Chrome not found in Applications"

    # Windows/Linux
    cmd = ["where", "chrome.exe"] if system == "Windows" else ["which", "google-chrome"]
    try:
        subprocess.run(cmd, check=True, capture_output=True, timeout=5)
        return True, "✅ Chrome detected"
    except:
        return False, "❌ Chrome not found in PATH"


def get_installation_commands() -> Dict[str, str]:
    """Get OS-specific installation commands"""
    system = platform.system()
    return {
        "Windows": (
            "Install missing components:\n"
            "1. Chrome: https://www.google.com/chrome/\n"
            "2. Allure: choco install allure-commandline OR scoop install allure"
        ),
        "Darwin": (
            "Install missing components:\n"
            "1. Chrome: brew install --cask google-chrome\n"
            "2. Allure: brew install allure"
        ),
        "Linux": (
            "Install missing components:\n"
            "1. Chrome: sudo apt install google-chrome-stable\n"
            "2. Allure:\n"
            "   sudo apt-add-repository ppa:qameta/allure\n"
            "   sudo apt-get update\n"
            "   sudo apt-get install allure"
        )
    }.get(system, "Please check documentation for your OS")


def main() -> int:
    """Main execution function"""
    print_header("Python-Selenium-POM Environment Check")

    # Run all checks
    checks = {
        "Python Version": check_python_version(),
        "Python Packages": check_packages(),
        "Allure CLI": check_allure(),
        "Chrome Browser": check_chrome()
    }

    # Display results
    all_passed = True
    for name, (passed, message) in checks.items():
        if isinstance(message, list):
            print_header(name)
            for m in message:
                print(m)
                if "❌" in m:
                    all_passed = False
        else:
            print(f"{name}: {message}")
            if not passed:
                all_passed = False

    # Final summary
    if all_passed:
        print_header("✅ All checks passed! You're ready to run Tests.")
        return 0

    print_header("❌ Some requirements are missing")
    print(get_installation_commands())
    print("\nNote: If Chrome is installed but not detected, Tests may still work")
    return 1


if __name__ == "__main__":
    sys.exit(main())
