# cleanup.py
import os
import platform
import time


def cleanup_chrome_processes():
    """Kill any existing Chrome and chromedriver processes."""
    print("Cleaning up Chrome processes...")

    if platform.system() == "Windows":
        os.system("taskkill /f /im chrome.exe /t")
        os.system("taskkill /f /im chromedriver.exe /t")
    else:
        os.system("pkill -f chrome || true")
        os.system("pkill -f chromedriver || true")

    # Give the system a moment to actually kill processes
    time.sleep(2)
    print("Cleanup complete")


if __name__ == "__main__":
    cleanup_chrome_processes()