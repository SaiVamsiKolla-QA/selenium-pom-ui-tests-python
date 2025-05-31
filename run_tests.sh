#!/usr/bin/env bash

BROWSER_TO_USE="${BROWSER:-chrome}"
SELENIUM_REMOTE_URL_TO_USE="${SELENIUM_REMOTE_URL}"
PYTEST_ARGS=("Tests/") # Default test path

# Initialize custom arguments
CUSTOM_NUM_PROCESSES=""
CUSTOM_ALLURE_DIR=""

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -n|--numprocesses)
      CUSTOM_NUM_PROCESSES="$2"
      shift # past argument
      shift # past value
      ;;
    --alluredir=*)
      CUSTOM_ALLURE_DIR="${1#*=}"
      shift # past argument=value
      ;;
    *) # Default case: unknown options or test paths
      PYTEST_ARGS+=("$1") # Add it to pytest arguments
      shift # past argument
      ;;
  esac
done

PYTEST_ARGS+=(--browser="$BROWSER_TO_USE")

if [ -n "$SELENIUM_REMOTE_URL_TO_USE" ]; then
  PYTEST_ARGS+=(--remote-url="$SELENIUM_REMOTE_URL_TO_USE")
fi

if [ -n "$CUSTOM_NUM_PROCESSES" ]; then
  PYTEST_ARGS+=(-n "$CUSTOM_NUM_PROCESSES")
fi

if [ -n "$CUSTOM_ALLURE_DIR" ]; then
  PYTEST_ARGS+=(--alluredir="$CUSTOM_ALLURE_DIR")
fi

echo "Effective BROWSER: $BROWSER_TO_USE"
echo "Effective SELENIUM_REMOTE_URL: $SELENIUM_REMOTE_URL_TO_USE"
echo "Running command: pytest ${PYTEST_ARGS[*]}"

# Execute pytest with the constructed arguments
pytest "${PYTEST_ARGS[@]}"
