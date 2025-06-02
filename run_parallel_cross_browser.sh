#!/bin/bash

# Default values
WORKERS=4
REMOTE_URL="http://localhost:4444/wd/hub"
BROWSERS=("chrome" "firefox")
TEST_PATH="Tests/"
ALLURE_RESULTS_DIR="allure-results"
ALLURE_REPORT_DIR="allure-report/multi-browser"

# Help function
show_help() {
    echo "Usage: ./run_parallel_cross_browser.sh [options]"
    echo "Options:"
    echo "  -w, --workers N        Number of parallel workers (default: 4)"
    echo "  -b, --browsers LIST    Comma-separated list of browsers (default: chrome,firefox)"
    echo "  -u, --url URL         Remote Selenium Grid URL (default: http://localhost:4444/wd/hub)"
    echo "  -t, --tests PATH      Test path (default: Tests/)"
    echo "  -h, --help           Show this help message"
    echo ""
    echo "Example:"
    echo "  ./run_parallel_cross_browser.sh -w 6 -b chrome,firefox,edge"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -w|--workers)
            WORKERS="$2"
            shift 2
            ;;
        -b|--browsers)
            IFS=',' read -ra BROWSERS <<< "$2"
            shift 2
            ;;
        -u|--url)
            REMOTE_URL="$2"
            shift 2
            ;;
        -t|--tests)
            TEST_PATH="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Print configuration
echo "🚀 Starting Parallel Cross-Browser Tests"
echo "======================================="
echo "Workers per browser: $WORKERS"
echo "Browsers: ${BROWSERS[*]}"
echo "Remote URL: $REMOTE_URL"
echo "Test Path: $TEST_PATH"
echo "---------------------------------------"

# Clean previous results
rm -rf "$ALLURE_RESULTS_DIR"/*
mkdir -p "$ALLURE_RESULTS_DIR"

# Run tests for each browser in parallel
for browser in "${BROWSERS[@]}"; do
    echo "Starting tests for $browser..."
    pytest -n "$WORKERS" \
          --dist=loadfile \
          --browser="$browser" \
          --remote-url="$REMOTE_URL" \
          --alluredir="$ALLURE_RESULTS_DIR/$browser" \
          "$TEST_PATH" -v &
done

# Wait for all parallel processes to complete
wait

echo "---------------------------------------"
echo "All browser tests completed!"
echo "Generating Allure report..."

# Generate combined Allure report
allure_results_paths=""
for browser in "${BROWSERS[@]}"; do
    allure_results_paths+="$ALLURE_RESULTS_DIR/$browser "
done

allure generate $allure_results_paths -o "$ALLURE_REPORT_DIR" --clean

echo "Opening Allure report..."
allure open "$ALLURE_REPORT_DIR" 