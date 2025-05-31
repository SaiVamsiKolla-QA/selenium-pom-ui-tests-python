#!/usr/bin/env bash

# Determine the browser to use
# Default to "chrome" if BROWSER is unset or empty
BROWSER_TO_USE="${BROWSER:-chrome}"
if [ -z "$BROWSER_TO_USE" ]; then
  BROWSER_TO_USE="chrome"
fi

# Determine the Selenium remote URL to use
# Default to an empty string if SELENIUM_REMOTE_URL is unset or empty
SELENIUM_REMOTE_URL_TO_USE="${SELENIUM_REMOTE_URL}"

# Construct the base pytest command
pytest_command="pytest tests/ --browser=\"$BROWSER_TO_USE\""

# Append Selenium remote URL if it's set
if [ -n "$SELENIUM_REMOTE_URL_TO_USE" ]; then
  pytest_command="$pytest_command --remote-url=\"$SELENIUM_REMOTE_URL_TO_USE\""
fi

# Echo the command
echo "Running command: $pytest_command"

# Execute the command
eval "$pytest_command"
