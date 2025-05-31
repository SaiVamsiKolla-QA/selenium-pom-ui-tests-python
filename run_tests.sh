#!/usr/bin/env bash

# ============================================================================
# Test Runner Script - Multi-Browser Test Automation with Allure Reporting
# ============================================================================
# Purpose: Automates pytest execution across multiple browsers with advanced
#          reporting, parallel execution, and statistical analysis
#
# Features:
# - Single and multi-browser test execution
# - Parallel execution at browser and test levels
# - Allure report generation with history tracking
# - Statistical analysis of test execution times
# - Graceful handling of missing browsers
# ============================================================================

# Enable strict error handling for reliability
set -o pipefail  # Pipe failures will be caught
set -o errtrace  # ERR trap is inherited by functions

# --- DEFAULT CONFIGURATION ---
# These values are used when no command-line arguments are provided
DEFAULT_ITERATIONS=1          # Number of times to run each test
DEFAULT_BROWSER="chrome"      # Default browser for single-browser mode
DEFAULT_PARALLEL=""          # Empty means sequential execution
DEFAULT_TEST_PATH="Tests/"   # Default directory containing test files
OPEN_REPORT=false           # Whether to auto-open Allure report
NO_REPORT=false            # Whether to skip report generation
ALL_BROWSERS=false         # Whether to test on all browsers
PARALLEL_BROWSERS=false    # Whether to run browsers simultaneously

# Browser configurations
# Note: Safari often has issues with parallel execution, consider excluding from PARALLEL_BROWSER_LIST
BROWSER_LIST=("chrome" "firefox" "edge" "safari")              # All available browsers
PARALLEL_BROWSER_LIST=("chrome" "firefox" "edge" "safari")     # Browsers safe for parallel execution

# --- COLOR CODES FOR TERMINAL OUTPUT ---
# ANSI color codes for better readability in terminal
RED='\033[0;31m'     # Error messages
GREEN='\033[0;32m'   # Success messages
YELLOW='\033[1;33m'  # Warnings
BLUE='\033[0;34m'    # Information
PURPLE='\033[0;35m'  # Execution time
CYAN='\033[0;36m'    # Headers
NC='\033[0m'         # No Color (reset)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

# Function: usage
# Description: Displays comprehensive help information about script usage
# Parameters: None
# Returns: None
usage() {
    echo "🚀 Test Runner with Allure Reporting"
    echo ""
    echo "Usage: $0 [TEST_PATH] [OPTIONS]"
    echo ""
    echo "Arguments:"
    echo "  TEST_PATH              Path to test file or directory (default: Tests/)"
    echo ""
    echo "Options:"
    echo "  -n, --iterations N     Number of test iterations (default: 1)"
    echo "  -b, --browser BROWSER  Browser: chrome, firefox, edge, safari (default: chrome)"
    echo "  --all-browsers         Run tests on ALL browsers (chrome, firefox, edge, safari)"
    echo "  --parallel-browsers    Run browsers simultaneously"
    echo "  -p, --parallel N       Number of parallel workers within each browser (default: sequential)"
    echo "  -o, --open-report      Automatically open Allure report (uses results with history)"
    echo "  --no-report           Skip Allure report generation"
    echo "  -h, --help            Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                                                    # Run all tests once"
    echo "  $0 Tests/test_swag_login.py -n 5                     # Run specific test 5 times"
    echo "  $0 Tests/ -n 5 -b chrome -p 6 -o                    # Parallel execution with report"
    echo "  $0 Tests/test_swag_login.py --all-browsers --parallel-browsers -n 2 -o  # Parallel browsers!"
}

# Function: copy_allure_history
# Description: Copies Allure history from previous report to enable trend analysis
# Parameters:
#   $1 - allure_results_dir: Directory where current test results are stored
#   $2 - persistent_report_dir: Directory containing previous report with history
# Returns: None
# Note: History allows Allure to show trends across multiple test runs
copy_allure_history() {
    local allure_results_dir="$1"
    local persistent_report_dir="$2"

    # Check if previous history exists
    if [ -d "$persistent_report_dir/history" ]; then
        echo -e "${BLUE}🔄 Copying history from previous report ($persistent_report_dir/history) for trend...${NC}"

        # Ensure target directory exists
        mkdir -p "$allure_results_dir/history"

        # Copy all history files, preserving structure
        # Using /. pattern to copy contents, not the directory itself
        cp -R "$persistent_report_dir/history/." "$allure_results_dir/history/" 2>/dev/null || {
            echo -e "${YELLOW}⚠️  Warning: Failed to copy some history files${NC}"
        }
    else
        echo -e "${YELLOW}🤔 No previous history found at $persistent_report_dir/history to generate trend.${NC}"
    fi
}

# Function: prepare_allure_results_directory
# Description: Prepares directory for new test results while preserving history
# Parameters:
#   $1 - current_allure_results_dir: Directory to prepare
#   $2 - source_persistent_report_dir_for_history: Source for history (used if NO_REPORT is false)
# Returns: None
# Note: Careful not to delete history subdirectory during cleanup
prepare_allure_results_directory() {
    local current_allure_results_dir="$1"
    local source_persistent_report_dir_for_history="$2"

    echo -e "${YELLOW}🗑️ Preparing Allure results directory: $current_allure_results_dir...${NC}"

    # Clean previous pytest results while preserving history
    if [ -d "$current_allure_results_dir" ]; then
        # Find and delete all files/dirs except 'history'
        # Using -mindepth 1 -maxdepth 1 to only look at direct children
        find "$current_allure_results_dir" -mindepth 1 -maxdepth 1 ! -name 'history' -exec rm -rf {} + 2>/dev/null || {
            echo -e "${YELLOW}⚠️  Warning: Some files couldn't be cleaned${NC}"
        }
    fi

    # Ensure directory exists with proper permissions
    mkdir -p "$current_allure_results_dir" || {
        echo -e "${RED}❌ Error: Cannot create results directory${NC}"
        exit 1
    }

    # Copy history if report generation is enabled
    if [ "$NO_REPORT" = false ]; then
        # Only copy history if it doesn't already exist in results dir
        if [ ! -d "$current_allure_results_dir/history" ]; then
             copy_allure_history "$current_allure_results_dir" "$source_persistent_report_dir_for_history"
        fi
    fi
}

# Function: generate_and_serve_allure_report
# Description: Generates Allure report and optionally serves it via web server
# Parameters:
#   $1 - allure_results_dir: Directory containing test results
#   $2 - persistent_report_dir: Output directory for generated report
#   $3 - report_title_prefix: Descriptive prefix for report (e.g., "Single Browser")
# Returns: None
generate_and_serve_allure_report() {
    local allure_results_dir="$1"
    local persistent_report_dir="$2"
    local report_title_prefix="$3"

    echo ""
    echo -e "${CYAN}🔄 Generating $report_title_prefix Allure Report...${NC}"

    # Ensure output directory exists
    mkdir -p "$persistent_report_dir" || {
        echo -e "${RED}❌ Error: Cannot create report directory${NC}"
        return 1
    }

    # Generate the report
    # --clean flag ensures old report data is removed
    if allure generate "$allure_results_dir" -o "$persistent_report_dir" --clean >/dev/null 2>&1; then
        echo -e "${GREEN}✅ $report_title_prefix Allure Report Generated Successfully!${NC}"
        echo -e "${BLUE}📁 Report Location: $persistent_report_dir${NC}"

        # Serve report if requested
        if [ "$OPEN_REPORT" = true ]; then
            echo -e "${PURPLE}🌐 Opening $report_title_prefix Report (using results from $allure_results_dir)...${NC}"

            # Start Allure web server in background
            # Note: Serving from results dir preserves test attachments
            allure serve "$allure_results_dir" &
            local allure_pid=$!

            # Give server time to start
            sleep 2

            # Check if server started successfully
            if kill -0 $allure_pid 2>/dev/null; then
                echo -e "${GREEN}✅ Report server started. Press Ctrl+C to stop when done.${NC}"
                wait $allure_pid  # Wait for user to stop server
            else
                echo -e "${RED}❌ Failed to start Allure server${NC}"
            fi
        fi
    else
        echo -e "${RED}❌ Error generating Allure report${NC}"
        echo -e "${YELLOW}   Tip: Check if allure-results directory contains valid test results${NC}"
    fi
}

# ============================================================================
# ALLURE METADATA FILE CREATORS
# These functions create metadata files that enhance Allure reports
# ============================================================================

# Function: create_environment_file
# Description: Creates environment.properties file for Allure report metadata
# Parameters:
#   $1 - results_dir: Directory to create file in
#   $2 - browser: Browser name
#   $3 - iterations: Number of test iterations
#   $4 - parallel: Number of parallel workers (optional)
create_environment_file() {
    local results_dir="$1"
    local browser="$2"
    local iterations="$3"
    local parallel="$4"

    # Capitalize browser name for display
    local browser_cap=$(echo "${browser:0:1}" | tr '[:lower:]' '[:upper:]')${browser:1}

    # Write environment properties
    cat > "$results_dir/environment.properties" << EOF
Browser=$browser_cap
Environment=Test
Python.Version=$(python --version 2>&1 | cut -d' ' -f2)
Operating.System=$(uname -s) $(uname -r)
Architecture=$(uname -m)
Test.Iterations=$iterations
Parallel.Workers=${parallel:-Sequential}
Execution.Date=$(date '+%Y-%m-%d %H:%M:%S')
Base.URL=https://www.saucedemo.com/
EOF
}

# Function: create_categories_file
# Description: Creates categories.json for test categorization in Allure
# Parameters:
#   $1 - results_dir: Directory to create file in
# Note: Categories help organize tests by type in Allure report
create_categories_file() {
    local results_dir="$1"

    cat > "$results_dir/categories.json" << 'EOF'
[
  {"name": "Login Tests", "matchedStatuses": ["passed", "failed", "broken"], "messageRegex": ".*login.*"},
  {"name": "E2E Tests", "matchedStatuses": ["passed", "failed", "broken"], "messageRegex": ".*end_to_end.*"},
  {"name": "Checkout Tests", "matchedStatuses": ["passed", "failed", "broken"], "messageRegex": ".*checkout.*"},
  {"name": "Product Page Tests", "matchedStatuses": ["passed", "failed", "broken"], "messageRegex": ".*product.*"},
  {"name": "Browser Issues", "matchedStatuses": ["failed", "broken"], "messageRegex": ".*WebDriver.*|.*browser.*|.*selenium.*"}
]
EOF
}

# Function: create_executor_file
# Description: Creates executor.json with build information for single browser mode
# Parameters:
#   $1 - results_dir: Directory to create file in
#   $2 - browser: Browser name
#   $3 - iterations: Number of iterations
#   $4 - start_time: Execution start time (seconds since epoch)
#   $5 - end_time: Execution end time (seconds since epoch)
create_executor_file() {
    local results_dir="$1"
    local browser="$2"
    local iterations="$3"
    local start_time="$4"
    local end_time="$5"

    # Capitalize browser name
    local browser_cap=$(echo "${browser:0:1}" | tr '[:lower:]' '[:upper:]')${browser:1}

    # Convert to milliseconds for Allure
    local start_ms=$((start_time * 1000))
    local end_ms=$((end_time * 1000))
    local build_order=$(date +%s)

    # Create compact JSON
    cat > "$results_dir/executor.json" << EOF
{"name": "Single Browser Test Executor", "type": "bash", "buildOrder": $build_order,
 "buildName": "$browser_cap - $iterations iterations", "buildUrl": "file://$(pwd)",
 "reportName": "Allure Report - $browser_cap", "reportUrl": "", "startedAt": $start_ms, "endedAt": $end_ms}
EOF
}

# Function: create_multi_browser_environment_file
# Description: Creates environment file for multi-browser test runs
# Parameters:
#   $1 - results_dir: Directory to create file in
#   $2 - iterations: Iterations per browser
#   $3 - parallel: Parallel workers per browser
#   $4 - mode: "parallel" or "sequential"
create_multi_browser_environment_file() {
    local results_dir="$1"
    local iterations="$2"
    local parallel="$3"
    local mode="$4"

    # Determine which browser list was used based on mode
    local browsers_tested_list_str
    local num_browsers

    if [ "$mode" = "parallel" ]; then
        browsers_tested_list_str="${PARALLEL_BROWSER_LIST[*]}"
        num_browsers=${#PARALLEL_BROWSER_LIST[@]}
    else
        browsers_tested_list_str="${BROWSER_LIST[*]}"
        num_browsers=${#BROWSER_LIST[@]}
    fi

    # Calculate total iterations across all browsers
    local total_suite_iterations=$((iterations * num_browsers))

    cat > "$results_dir/environment.properties" << EOF
Test.Type=Multi-Browser ($mode)
Browsers.Attempted=$browsers_tested_list_str
Environment=Test
Python.Version=$(python --version 2>&1 | cut -d' ' -f2)
Operating.System=$(uname -s) $(uname -r)
Architecture=$(uname -m)
Iterations.Per.Browser=$iterations
Total.Suite.Iterations=$total_suite_iterations
Parallel.Workers.Per.Browser=${parallel:-Sequential}
Execution.Date=$(date '+%Y-%m-%d %H:%M:%S')
Base.URL=https://www.saucedemo.com/
EOF
}

# Function: create_all_browsers_executor_file
# Description: Creates executor.json for multi-browser runs
# Parameters:
#   $1 - results_dir: Directory to create file in
#   $2 - iterations_per_browser: Iterations for each browser
#   $3 - start_time_sec: Start time in seconds
#   $4 - end_time_sec: End time in seconds
#   $5 - mode: "parallel" or "sequential"
create_all_browsers_executor_file() {
    local results_dir="$1"
    local iterations_per_browser="$2"
    local start_time_sec="$3"
    local end_time_sec="$4"
    local mode="$5"

    # Convert times to milliseconds
    local start_ms=$((start_time_sec * 1000))
    local end_ms=$((end_time_sec * 1000))
    local build_order=$(date +%s)

    # Set appropriate labels based on mode
    local build_name_prefix
    local report_name_prefix
    local browser_list_for_calc_array

    if [ "$mode" = "parallel" ]; then
        build_name_prefix="Parallel Multi-Browser"
        report_name_prefix="Parallel Multi-Browser"
        browser_list_for_calc_array=("${PARALLEL_BROWSER_LIST[@]}")
    else
        build_name_prefix="Sequential Multi-Browser"
        report_name_prefix="Sequential Multi-Browser"
        browser_list_for_calc_array=("${BROWSER_LIST[@]}")
    fi

    # Calculate total iterations
    local total_suite_iterations=$((iterations_per_browser * ${#browser_list_for_calc_array[@]}))

    cat > "$results_dir/executor.json" << EOF
{"name": "$build_name_prefix Test Executor", "type": "bash", "buildOrder": $build_order,
 "buildName": "$build_name_prefix - $total_suite_iterations total suite iterations", "buildUrl": "file://$(pwd)",
 "reportName": "$report_name_prefix Allure Report", "reportUrl": "", "startedAt": $start_ms, "endedAt": $end_ms}
EOF
}

# ============================================================================
# CORE LOGIC FUNCTIONS
# ============================================================================

# Function: calculate_stats
# Description: Calculates statistical metrics from test durations
# Parameters:
#   $@ - Array of duration values
# Global outputs:
#   STAT_AVG - Average duration
#   STAT_MIN - Minimum duration
#   STAT_MAX - Maximum duration
#   STAT_STD_DEV - Standard deviation
calculate_stats() {
    local durations=("$@")
    local count=${#durations[@]}

    # Handle empty array
    if [ "$count" -eq 0 ]; then
        STAT_AVG=0
        STAT_MIN=0
        STAT_MAX=0
        STAT_STD_DEV=0
        return
    fi

    # Initialize variables
    local sum=0
    local min=${durations[0]}
    local max=${durations[0]}

    # First pass: calculate sum, min, max
    for duration in "${durations[@]}"; do
        # Add to sum
        sum=$(echo "$sum + $duration" | bc -l)

        # Update min if current is smaller
        if (( $(echo "$duration < $min" | bc -l) )); then
            min=$duration
        fi

        # Update max if current is larger
        if (( $(echo "$duration > $max" | bc -l) )); then
            max=$duration
        fi
    done

    # Calculate average
    local avg=$(echo "scale=2; $sum / $count" | bc -l)

    # Second pass: calculate variance for standard deviation
    local variance_sum=0
    for duration in "${durations[@]}"; do
        local diff=$(echo "$duration - $avg" | bc -l)
        local squared=$(echo "$diff * $diff" | bc -l)
        variance_sum=$(echo "$variance_sum + $squared" | bc -l)
    done

    # Calculate variance and standard deviation
    local variance=$(echo "scale=4; $variance_sum / $count" | bc -l)
    local std_dev=$(echo "scale=2; sqrt($variance)" | bc -l)

    # Set global variables for return
    STAT_AVG=$avg
    STAT_MIN=$min
    STAT_MAX=$max
    STAT_STD_DEV=$std_dev
}

# Function: parse_arguments
# Description: Parses and validates command-line arguments
# Parameters:
#   $@ - All command-line arguments
# Global outputs:
#   TEST_PATH, ITERATIONS, BROWSER, PARALLEL, and flag variables
parse_arguments() {
    local test_path=""
    local iterations=$DEFAULT_ITERATIONS
    local browser=$DEFAULT_BROWSER
    local parallel=$DEFAULT_PARALLEL

    # Process arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -n|--iterations)
                iterations="$2"
                # Validate iterations is a positive integer
                if ! [[ "$iterations" =~ ^[0-9]+$ && "$iterations" -ge 1 ]]; then
                    echo -e "${RED}❌ Iterations: positive integer${NC}"
                    exit 1
                fi
                shift 2
                ;;

            -b|--browser)
                browser="$2"
                # Validate browser is in allowed list
                if [[ ! " ${BROWSER_LIST[*]} " =~ " $browser " ]]; then
                    echo -e "${RED}❌ Browser must be one of: ${BROWSER_LIST[*]}${NC}"
                    exit 1
                fi
                shift 2
                ;;

            -p|--parallel)
                parallel="$2"
                # Validate parallel is a positive integer
                if ! [[ "$parallel" =~ ^[0-9]+$ && "$parallel" -ge 1 ]]; then
                    echo -e "${RED}❌ Parallel workers: positive integer${NC}"
                    exit 1
                fi
                shift 2
                ;;

            -o|--open-report)
                OPEN_REPORT=true
                shift
                ;;

            --all-browsers)
                ALL_BROWSERS=true
                shift
                ;;

            --parallel-browsers)
                PARALLEL_BROWSERS=true
                shift
                ;;

            --no-report)
                NO_REPORT=true
                shift
                ;;

            -h|--help)
                usage
                exit 0
                ;;

            -*)
                echo -e "${RED}❌ Unknown option $1${NC}"
                usage
                exit 1
                ;;

            *)
                # Non-option argument (test path)
                if [ -z "$test_path" ]; then
                    test_path="$1"
                else
                    echo -e "${RED}❌ Multiple test paths specified${NC}"
                    usage
                    exit 1
                fi
                shift
                ;;
        esac
    done

    # Set global variables
    TEST_PATH=${test_path:-$DEFAULT_TEST_PATH}
    ITERATIONS=$iterations
    BROWSER=$browser
    PARALLEL=$parallel

    # Inform user about multi-browser mode
    if [ "$ALL_BROWSERS" = true ]; then
        echo -e "${YELLOW}ℹ️  Multi-browser mode selected. Individual browser setting ignored.${NC}"
        if [ "$PARALLEL_BROWSERS" = true ]; then
            echo -e "${YELLOW}   Type: Parallel${NC}"
        else
            echo -e "${YELLOW}   Type: Sequential${NC}"
        fi
    fi
}

# Function: run_single_browser_background
# Description: Runs tests for a single browser in background (for parallel execution)
# Parameters:
#   $1 - browser: Browser name
#   $2 - allure_output_dir: Directory for Allure results
#   $3 - result_summary_file: File to write summary results
# Note: This function is designed to run in background for parallel browser execution
run_single_browser_background() {
    local browser="$1"
    local allure_output_dir="$2"
    local result_summary_file="$3"

    echo -e "${CYAN}🚀 Starting parallel tests for $(echo "$browser" | tr '[:lower:]' '[:upper:]')${NC}"

    # Initialize counters and tracking variables
    local successes=0
    local failures=0
    local durations_arr=()
    local start_time=$(date +%s.%N)
    local browser_unavailable=false

    # Run iterations for this browser
    for (( i=1; i<=$ITERATIONS; i++ )); do
        # Build pytest command array for safer execution
        local pytest_cmd_arr=("pytest" "$TEST_PATH" "-v" "--browser" "$browser")

        # Add Allure directory if reporting is enabled
        if [ "$NO_REPORT" = false ]; then
            pytest_cmd_arr+=("--alluredir=$allure_output_dir")
        fi

        # Add parallel workers if specified
        if [ ! -z "$PARALLEL" ]; then
            pytest_cmd_arr+=("-n" "$PARALLEL")
        fi

        # Execute test and capture output
        local iter_start=$(date +%s.%N)
        local output_str
        local exit_c

        # Run pytest and capture both stdout and stderr
        if output_str=$("${pytest_cmd_arr[@]}" 2>&1); then
            exit_c=0
        else
            exit_c=$?
        fi

        # Check if browser is not available (early exit condition)
        if [ $exit_c -ne 0 ] && \
           [[ "$output_str" == *"browser"* ]] && \
           [[ "$output_str" == *"not found"* || \
              "$output_str" == *"cannot find"* || \
              "$output_str" == *"WebDriverException"* ]]; then
            echo -e "  ${YELLOW}⚠️  Browser $browser not available - skipping${NC}"
            browser_unavailable=true
            break
        fi

        # Calculate iteration duration
        local iter_end=$(date +%s.%N)
        local dur=$(echo "$iter_end - $iter_start" | bc -l)
        durations_arr+=($dur)

        # Update counters and display result
        if [ $exit_c -eq 0 ]; then
            echo -e "  [$(echo "$browser" | tr '[:lower:]' '[:upper:]')] Iter $i/$ITERATIONS: ${GREEN}✅ PASSED${NC} in $(printf '%.2f' $dur)s"
            ((successes++))
        else
            echo -e "  [$(echo "$browser" | tr '[:lower:]' '[:upper:]')] Iter $i/$ITERATIONS: ${RED}❌ FAILED${NC} in $(printf '%.2f' $dur)s"
            ((failures++))
        fi
    done

    # Calculate total time for this browser
    local total_time_browser=$(echo "$(date +%s.%N) - $start_time" | bc -l)

    # Calculate success rate
    local success_r=0
    if [ $ITERATIONS -gt 0 ] && [ $((successes + failures)) -gt 0 ]; then
        success_r=$(echo "scale=2; ($successes * 100) / $ITERATIONS" | bc -l)
    fi

    # Write results to summary file
    if [ "$browser_unavailable" = false ]; then
        # Format: browser:successes:failures:success_rate:total_time:duration_list
        echo "$browser:$successes:$failures:$success_r:$total_time_browser:${durations_arr[*]}" > "$result_summary_file"
        echo -e "${GREEN}[$(echo "$browser" | tr '[:lower:]' '[:upper:]')] ✅ Testing completed: $successes passed, $failures failed ($(printf '%.1f' $success_r)%)${NC}"
    else
        # Mark browser as skipped
        echo "$browser:0:0:0:0:" > "$result_summary_file"
        echo -e "${YELLOW}[$(echo "$browser" | tr '[:lower:]' '[:upper:]')] ⚠️  Testing skipped${NC}"
    fi
}

# ============================================================================
# MAIN EXECUTION MODES
# ============================================================================

# Function: run_parallel_browser_tests
# Description: Executes tests on multiple browsers simultaneously
# Global inputs: TEST_PATH, ITERATIONS, PARALLEL, NO_REPORT, OPEN_REPORT
# Note: Each browser runs in its own background process
run_parallel_browser_tests() {
    # Setup directories
    local results_dir="allure-results/parallel-multi-browser"
    local report_dir="allure-report/parallel-multi-browser"

    # Track execution time
    local overall_start_time=$(date +%s.%N)

    # Arrays to track background processes
    local pids=()
    local tmp_result_files=()

    # Display execution plan
    echo -e "${CYAN}🚀 Running Parallel Multi-Browser Test Suite${NC}"
    echo -e "${BLUE}📊 Test Path: $TEST_PATH | Iterations/Browser: $ITERATIONS | Browsers: ${PARALLEL_BROWSER_LIST[*]} | Workers/Browser: ${PARALLEL:-Seq}${NC}"
    echo "$(printf '=%.0s' {1..80})"

    # Prepare results directory
    prepare_allure_results_directory "$results_dir" "$report_dir"

    # Start all browsers in parallel
    echo -e "${CYAN}🚀 Starting all browsers in parallel...${NC}"

    for browser_item in "${PARALLEL_BROWSER_LIST[@]}"; do
        # Create temporary file for this browser's results
        local tmp_result_file
        tmp_result_file=$(mktemp "/tmp/browser_result_${browser_item}_XXXXXX.txt") || {
            echo -e "${RED}❌ Failed to create temp file for $browser_item${NC}"
            exit 1
        }
        tmp_result_files+=("$tmp_result_file")

        # Start browser test in background
        run_single_browser_background "$browser_item" "$results_dir" "$tmp_result_file" &
        local pid=$!
        pids+=($pid)

        echo -e "${BLUE}📱 Started $browser_item testing (PID: $pid)${NC}"
    done

    # Wait for all background processes to complete
    echo -e "${PURPLE}⏳ Waiting for all browsers to complete...${NC}"

    for pid in "${pids[@]}"; do
        wait "$pid" || {
            echo -e "${YELLOW}⚠️  Process $pid exited with error${NC}"
        }
    done

    # Calculate total execution time
    local overall_end_time=$(date +%s.%N)
    local overall_duration=$(echo "$overall_end_time - $overall_start_time" | bc -l)

    echo -e "${GREEN}🎉 All browsers completed processing!${NC}"

    # Collect and aggregate results from all browsers
    local total_successes=0
    local total_failures=0
    local all_run_durations=()
    local browser_summary_lines=()

    for i in "${!PARALLEL_BROWSER_LIST[@]}"; do
        local browser_name_from_list="${PARALLEL_BROWSER_LIST[$i]}"
        local file_to_read="${tmp_result_files[$i]}"

        if [ -f "$file_to_read" ]; then
            # Read browser results
            local line_content=$(cat "$file_to_read")

            # Parse results (format: browser:successes:failures:success_rate:total_time:durations)
            IFS=':' read -r parsed_browser s_count f_count s_rate t_time durations_list_str <<< "$line_content"

            # Process results if tests were run
            if [ "$s_count" -gt 0 ] || [ "$f_count" -gt 0 ]; then
                browser_summary_lines+=("$parsed_browser:$s_count:$f_count:$s_rate")
                total_successes=$((total_successes + s_count))
                total_failures=$((total_failures + f_count))

                # Parse individual test durations
                if [ ! -z "$durations_list_str" ]; then
                    IFS=' ' read -ra dur_arr <<< "$durations_list_str"
                    all_run_durations+=("${dur_arr[@]}")
                fi
            elif [ "$parsed_browser" != "" ]; then
                # Browser was skipped
                browser_summary_lines+=("$parsed_browser:0:0:0.0")
            fi

            # Clean up temp file
            rm -f "$file_to_read"
        fi
    done

    # Create Allure metadata files
    if [ "$NO_REPORT" = false ]; then
        create_multi_browser_environment_file "$results_dir" "$ITERATIONS" "$PARALLEL" "parallel"
        create_categories_file "$results_dir"
        create_all_browsers_executor_file "$results_dir" "$ITERATIONS" "${overall_start_time%.*}" "${overall_end_time%.*}" "parallel"
    fi

    # Calculate overall statistics
    if [ ${#all_run_durations[@]} -gt 0 ]; then
        calculate_stats "${all_run_durations[@]}"
    fi

    # Calculate overall success rate
    local success_rate_overall=0
    local total_ran_tests=$((total_successes + total_failures))
    if [ $total_ran_tests -gt 0 ]; then
        success_rate_overall=$(echo "scale=2; ($total_successes * 100) / $total_ran_tests" | bc -l)
    fi

    # Display comprehensive summary
    echo ""
    echo "$(printf '=%.0s' {1..80})"
    echo -e "${CYAN}📈 PARALLEL MULTI-BROWSER SUMMARY${NC}"
    echo "$(printf '=%.0s' {1..80})"
    echo -e "${BLUE}🌐 Browsers Attempted: ${PARALLEL_BROWSER_LIST[*]}${NC}"
    echo -e "${GREEN}📊 Overall Results (from ran tests): $total_successes passed, $total_failures failed${NC}"
    echo -e "${YELLOW}🎯 Overall Success Rate (from ran tests): $(printf '%.2f' $success_rate_overall)%${NC}"
    echo -e "${PURPLE}⏱️  Total Execution Time: $(printf '%.2f' $overall_duration)s${NC}"

    # Display statistics if available
    if [ ${#all_run_durations[@]} -gt 0 ]; then
        echo -e "${CYAN}📐 Avg Test Time: $(printf '%.2f' $STAT_AVG)s | Min: $(printf '%.2f' $STAT_MIN)s | Max: $(printf '%.2f' $STAT_MAX)s | StdDev: $(printf '%.2f' $STAT_STD_DEV)s${NC}"
    fi

    # Display per-browser breakdown
    echo ""
    echo -e "${CYAN}📊 Per-Browser Breakdown:${NC}"

    for summary_line in "${browser_summary_lines[@]}"; do
        IFS=':' read -r brw s_cnt f_cnt sr <<< "$summary_line"
        local brw_disp=$(echo "$brw" | tr '[:lower:]' '[:upper:]')

        if [ "$s_cnt" -eq 0 ] && [ "$f_cnt" -eq 0 ] && [ "$(echo "$sr == 0.0" | bc -l)" -eq 1 ]; then
            echo -e "  ${YELLOW}$brw_disp:${NC} Testing skipped or browser not available"
        else
            echo -e "  ${BLUE}$brw_disp:${NC} $s_cnt passed, $f_cnt failed ($(printf '%.1f' $sr)%)"
        fi
    done

    # Generate Allure report if enabled
    if [ "$NO_REPORT" = false ]; then
        generate_and_serve_allure_report "$results_dir" "$report_dir" "Parallel Multi-Browser"
    fi

    echo "$(printf '=%.0s' {1..80})"
    echo -e "${GREEN}🎉 Parallel Multi-Browser Execution Completed!${NC}"

    # Exit with appropriate status code
    if [ $total_failures -eq 0 ]; then
        exit 0
    else
        exit 1
    fi
}

# Function: run_multi_browser_tests
# Description: Executes tests on multiple browsers sequentially
# Global inputs: TEST_PATH, ITERATIONS, PARALLEL, NO_REPORT, OPEN_REPORT
# Note: Each browser completes all iterations before moving to next browser
run_multi_browser_tests() {
    # Setup directories
    local results_dir="allure-results/multi-browser"
    local report_dir="allure-report/multi-browser"

    # Initialize tracking variables
    local overall_start_time=$(date +%s.%N)
    local total_s=0  # Total successes
    local total_f=0  # Total failures
    local all_durs=()  # All test durations
    local browser_s_lines=()  # Browser summary lines

    # Display execution plan
    echo -e "${CYAN}🌐 Running Sequential Multi-Browser Test Suite${NC}"
    echo -e "${BLUE}📊 Test Path: $TEST_PATH | Iterations/Browser: $ITERATIONS | Browsers: ${BROWSER_LIST[*]} | Workers/Browser: ${PARALLEL:-Seq}${NC}"
    echo "$(printf '=%.0s' {1..80})"

    # Prepare results directory
    prepare_allure_results_directory "$results_dir" "$report_dir"

    # Run tests for each browser sequentially
    for browser_item in "${BROWSER_LIST[@]}"; do
        echo ""
        echo -e "${CYAN}🚀 Starting tests for $(echo "$browser_item" | tr '[:lower:]' '[:upper:]')${NC}"
        echo "$(printf -- '-%.0s' {1..50})"

        # Initialize browser-specific counters
        local browser_s_iter=0  # Browser successes
        local browser_f_iter=0  # Browser failures
        local browser_durs_iter=()  # Browser durations
        local browser_unavail=false

        # Run iterations for this browser
        for (( i=1; i<=$ITERATIONS; i++ )); do
            # Build pytest command
            local pytest_cmd_arr=("pytest" "$TEST_PATH" "-v" "--browser" "$browser_item")

            if [ "$NO_REPORT" = false ]; then
                pytest_cmd_arr+=("--alluredir=$results_dir")
            fi

            if [ ! -z "$PARALLEL" ]; then
                pytest_cmd_arr+=("-n" "$PARALLEL")
            fi

            # Execute test
            local iter_s=$(date +%s.%N)
            local out_str
            local ex_c

            if out_str=$("${pytest_cmd_arr[@]}" 2>&1); then
                ex_c=0
            else
                ex_c=$?
            fi

            # Check for browser availability issues
            if [ $ex_c -ne 0 ] && \
               [[ "$out_str" == *"browser"* ]] && \
               [[ "$out_str" == *"not found"* || \
                  "$out_str" == *"cannot find"* || \
                  "$out_str" == *"WebDriverException"* ]]; then
                echo -e "  ${YELLOW}⚠️  Browser $browser_item not available - skipping for this browser${NC}"
                browser_unavail=true
                break
            fi

            # Calculate duration
            local iter_e=$(date +%s.%N)
            local d=$(echo "$iter_e - $iter_s" | bc -l)
            browser_durs_iter+=($d)
            all_durs+=($d)

            # Update counters and display results
            if [ $ex_c -eq 0 ]; then
                echo -e "  Iter $i/$ITERATIONS ($(echo "$browser_item" | tr '[:lower:]' '[:upper:]')): ${GREEN}✅ PASSED${NC} in $(printf '%.2f' $d)s"
                ((browser_s_iter++))
                ((total_s++))
            else
                echo -e "  Iter $i/$ITERATIONS ($(echo "$browser_item" | tr '[:lower:]' '[:upper:]')): ${RED}❌ FAILED${NC} in $(printf '%.2f' $d)s"
                ((browser_f_iter++))
                ((total_f++))

                # Show error details if available
                if [[ "$out_str" == *"ERROR"* ]] || [[ "$out_str" == *"FAILED"* ]]; then
                    echo -e "     ${RED}Err: $(echo "$out_str" | grep -E "ERROR|FAILED" | head -1 | sed 's/^[[:space:]]*//')${NC}"
                fi
            fi
        done

        # Handle skipped browser
        if [ "$browser_unavail" = true ]; then
            browser_s_lines+=("$browser_item:0:0:0.0")
            continue
        fi

        # Calculate browser success rate
        local browser_sr_iter=0
        if [ $ITERATIONS -gt 0 ] && [ $((browser_s_iter + browser_f_iter)) -gt 0 ]; then
            browser_sr_iter=$(echo "scale=2; ($browser_s_iter * 100) / $ITERATIONS" | bc -l)
        fi

        # Store browser summary
        browser_s_lines+=("$browser_item:$browser_s_iter:$browser_f_iter:$browser_sr_iter")

        # Display browser summary
        echo -e "${BLUE}  Summary $(echo "$browser_item" | tr '[:lower:]' '[:upper:]'): $browser_s_iter passed, $browser_f_iter failed ($(printf '%.1f' $browser_sr_iter)%)${NC}"
    done

    # Calculate total execution time
    local overall_e_time=$(date +%s.%N)
    local overall_dur=$(echo "$overall_e_time - $overall_start_time" | bc -l)

    # Create Allure metadata files
    if [ "$NO_REPORT" = false ]; then
        create_multi_browser_environment_file "$results_dir" "$ITERATIONS" "$PARALLEL" "sequential"
        create_categories_file "$results_dir"
        create_all_browsers_executor_file "$results_dir" "$ITERATIONS" "${overall_start_time%.*}" "${overall_e_time%.*}" "sequential"
    fi

    # Calculate overall statistics
    if [ ${#all_durs[@]} -gt 0 ]; then
        calculate_stats "${all_durs[@]}"
    fi

    # Calculate overall success rate
    local sr_overall=0
    local total_ran_t=$((total_s + total_f))
    if [ $total_ran_t -gt 0 ]; then
        sr_overall=$(echo "scale=2; ($total_s * 100) / $total_ran_t" | bc -l)
    fi

    # Display comprehensive summary
    echo ""
    echo "$(printf '=%.0s' {1..80})"
    echo -e "${CYAN}📈 SEQUENTIAL MULTI-BROWSER SUMMARY${NC}"
    echo "$(printf '=%.0s' {1..80})"
    echo -e "${BLUE}🌐 Browsers Attempted: ${BROWSER_LIST[*]}${NC}"
    echo -e "${GREEN}📊 Overall Results (from ran tests): $total_s passed, $total_f failed${NC}"
    echo -e "${YELLOW}🎯 Overall Success Rate (from ran tests): $(printf '%.2f' $sr_overall)%${NC}"
    echo -e "${PURPLE}⏱️  Total Execution Time: $(printf '%.2f' $overall_dur)s${NC}"

    # Display statistics if available
    if [ ${#all_durs[@]} -gt 0 ]; then
         echo -e "${CYAN}📐 Avg Test Time: $(printf '%.2f' $STAT_AVG)s | Min: $(printf '%.2f' $STAT_MIN)s | Max: $(printf '%.2f' $STAT_MAX)s | StdDev: $(printf '%.2f' $STAT_STD_DEV)s${NC}"
    fi

    # Display per-browser breakdown
    echo ""
    echo -e "${CYAN}📊 Per-Browser Breakdown:${NC}"

    for s_line in "${browser_s_lines[@]}"; do
        IFS=':' read -r brw s_c f_c sr <<< "$s_line"
        local brw_d=$(echo "$brw" | tr '[:lower:]' '[:upper:]')

        if [ "$s_c" -eq 0 ] && [ "$f_c" -eq 0 ] && [ "$(echo "$sr == 0.0" | bc -l)" -eq 1 ]; then
            echo -e "  ${YELLOW}$brw_d:${NC} Testing skipped or browser not available"
        else
            echo -e "  ${BLUE}$brw_d:${NC} $s_c passed, $f_c failed ($(printf '%.1f' $sr)%)"
        fi
    done

    # Generate Allure report if enabled
    if [ "$NO_REPORT" = false ]; then
        generate_and_serve_allure_report "$results_dir" "$report_dir" "Sequential Multi-Browser"
    fi

    echo "$(printf '=%.0s' {1..80})"
    echo -e "${GREEN}🎉 Sequential Multi-Browser Execution Completed!${NC}"

    # Exit with appropriate status code
    if [ $total_f -eq 0 ]; then
        exit 0
    else
        exit 1
    fi
}

# Function: run_tests
# Description: Executes tests for a single browser
# Global inputs: TEST_PATH, BROWSER, ITERATIONS, PARALLEL, NO_REPORT, OPEN_REPORT
# Note: Main function for single-browser test execution
run_tests() {
    # Validate test path exists
    if [ ! -e "$TEST_PATH" ]; then
        echo -e "${RED}❌ Test path '$TEST_PATH' not found${NC}"
        echo -e "${YELLOW}   Available test files:${NC}"
        find Tests/ -name "*.py" -type f 2>/dev/null | head -10 || echo "   No test files found in Tests/"
        exit 1
    fi

    # Setup directories
    local results_dir="allure-results/$BROWSER"
    local report_dir="allure-report/$BROWSER"

    # Display execution plan
    echo -e "${CYAN}🚀 Running Single Browser: $(echo "$BROWSER" | tr '[:lower:]' '[:upper:]')${NC}"
    echo -e "${BLUE}📊 Path: $TEST_PATH | Iterations: $ITERATIONS | Workers: ${PARALLEL:-Sequential}${NC}"
    echo -e "${YELLOW}📁 Allure Results: $results_dir | Report: $report_dir${NC}"
    echo "$(printf '=%.0s' {1..80})"

    # Clean up browser processes
    if [ -f "cleanup.py" ]; then
        echo -e "${CYAN}🧹 Running cleanup.py...${NC}"
        python cleanup.py
    else
        echo -e "${CYAN}🧹 Cleaning $BROWSER processes...${NC}"
        pkill -f "$BROWSER" 2>/dev/null || true
        echo "Cleanup done."
    fi

    # Prepare results directory
    prepare_allure_results_directory "$results_dir" "$report_dir"

    # Create Allure metadata files
    if [ "$NO_REPORT" = false ]; then
        echo -e "${BLUE}📝 Creating Allure metadata...${NC}"
        create_environment_file "$results_dir" "$BROWSER" "$ITERATIONS" "$PARALLEL"
        create_categories_file "$results_dir"
    fi

    # Initialize counters
    local s_count=0  # Success count
    local f_count=0  # Failure count
    local durs_arr=()  # Duration array
    local overall_s_time=$(date +%s.%N)

    # Run test iterations
    for (( i=1; i<=$ITERATIONS; i++ )); do
        # Build pytest command
        local pytest_cmd_arr=("pytest" "$TEST_PATH" "-v" "--browser" "$BROWSER")

        if [ "$NO_REPORT" = false ]; then
            pytest_cmd_arr+=("--alluredir=$results_dir")
        fi

        if [ ! -z "$PARALLEL" ]; then
            pytest_cmd_arr+=("-n" "$PARALLEL")
        fi

        # Execute test
        local iter_s_time=$(date +%s.%N)
        local py_output
        local py_exit_c

        if py_output=$("${pytest_cmd_arr[@]}" 2>&1); then
            py_exit_c=0
        else
            py_exit_c=$?
        fi

        # Calculate duration
        local iter_e_time=$(date +%s.%N)
        local iter_dur=$(echo "$iter_e_time - $iter_s_time" | bc -l)
        durs_arr+=($iter_dur)

        # Update counters and display results
        if [ $py_exit_c -eq 0 ]; then
            echo -e "Iter $i/$ITERATIONS: ${GREEN}✅ PASSED${NC} in $(printf '%.2f' $iter_dur)s"
            ((s_count++))
        else
            echo -e "Iter $i/$ITERATIONS: ${RED}❌ FAILED${NC} in $(printf '%.2f' $iter_dur)s"
            ((f_count++))

            # Show error details if available
            if [[ "$py_output" == *"ERROR"* ]] || [[ "$py_output" == *"FAILED"* ]]; then
                echo -e "   ${RED}Err: $(echo "$py_output" | grep -E "ERROR|FAILED" | head -1 | sed 's/^[[:space:]]*//')${NC}"
            fi
        fi
    done

    # Calculate total execution time
    local overall_e_time=$(date +%s.%N)
    local overall_d=$(echo "$overall_e_time - $overall_s_time" | bc -l)

    # Create executor file
    if [ "$NO_REPORT" = false ]; then
        create_executor_file "$results_dir" "$BROWSER" "$ITERATIONS" "${overall_s_time%.*}" "${overall_e_time%.*}"
    fi

    # Calculate statistics
    calculate_stats "${durs_arr[@]}"

    # Calculate success rate
    local s_rate_final=0
    if [ $ITERATIONS -gt 0 ]; then
        s_rate_final=$(echo "scale=2; ($s_count * 100) / $ITERATIONS" | bc -l)
    fi

    # Display summary
    echo ""
    echo "$(printf '=%.0s' {1..80})"
    echo -e "${CYAN}📈 SINGLE BROWSER SUMMARY (${BROWSER^^})${NC}"
    echo "$(printf '=%.0s' {1..80})"
    echo -e "${GREEN}📊 Results: $s_count passed, $f_count failed | ${YELLOW}🎯 Success: $(printf '%.2f' $s_rate_final)%${NC}"
    echo -e "${PURPLE}⏱️  Total Time: $(printf '%.2f' $overall_d)s${NC}"
    echo -e "${CYAN}📐 Avg Test Time: $(printf '%.2f' $STAT_AVG)s | Min: $(printf '%.2f' $STAT_MIN)s | Max: $(printf '%.2f' $STAT_MAX)s | StdDev: $(printf '%.2f' $STAT_STD_DEV)s${NC}"

    # Generate Allure report if enabled
    if [ "$NO_REPORT" = false ]; then
        generate_and_serve_allure_report "$results_dir" "$report_dir" "Single Browser (${BROWSER^^})"
    fi

    echo "$(printf '=%.0s' {1..80})"
    echo -e "${GREEN}🎉 Test execution completed.${NC}"

    # Exit with appropriate status code
    if [ $f_count -eq 0 ]; then
        exit 0
    else
        exit 1
    fi
}

# Function: check_dependencies
# Description: Verifies all required dependencies are installed
# Returns: Exits with error if dependencies are missing
check_dependencies() {
    local missing_deps=()

    # Check Python
    if ! command -v python >/dev/null 2>&1; then
        missing_deps+=("python")
    fi

    # Check pytest
    if ! python -c "import pytest" >/dev/null 2>&1; then
        missing_deps+=("pytest (python package)")
    fi

    # Check bc for calculations
    if ! command -v bc >/dev/null 2>&1; then
        missing_deps+=("bc")
    fi

    # Check for allure only if report generation is not skipped
    if [ "$NO_REPORT" = false ] && ! command -v allure >/dev/null 2>&1; then
        missing_deps+=("allure (command line tool)")
    fi

    # Display error if dependencies are missing
    if [ ${#missing_deps[@]} -gt 0 ]; then
        echo -e "${RED}❌ Missing dependencies: ${missing_deps[*]}${NC}"
        echo -e "${YELLOW}Please install them to continue:${NC}"
        echo ""

        # Provide installation hints
        for dep in "${missing_deps[@]}"; do
            case "$dep" in
                "python")
                    echo "  • Python: https://www.python.org/downloads/"
                    ;;
                "pytest (python package)")
                    echo "  • pytest: pip install pytest pytest-xdist"
                    ;;
                "bc")
                    echo "  • bc: apt-get install bc (Linux) or brew install bc (macOS)"
                    ;;
                "allure (command line tool)")
                    echo "  • Allure: brew install allure (macOS) or see https://docs.qameta.io/allure/"
                    ;;
            esac
        done

        exit 1
    fi
}

# Function: main
# Description: Main entry point - coordinates script execution
# Parameters:
#   $@ - All command-line arguments
main() {
    # Handle no arguments case - use all defaults
    if [ $# -eq 0 ]; then
        TEST_PATH=$DEFAULT_TEST_PATH
        ITERATIONS=$DEFAULT_ITERATIONS
        BROWSER=$DEFAULT_BROWSER
        PARALLEL=$DEFAULT_PARALLEL
        ALL_BROWSERS=false
        PARALLEL_BROWSERS=false
    else
        # Parse provided arguments
        parse_arguments "$@"
    fi

    # Check dependencies after parsing (respects NO_REPORT flag)
    check_dependencies

    # Route to appropriate execution mode
    if [ "$ALL_BROWSERS" = true ]; then
        # Multi-browser mode
        if [ "$PARALLEL_BROWSERS" = true ]; then
            # Run browsers in parallel
            run_parallel_browser_tests
        else
            # Run browsers sequentially
            run_multi_browser_tests
        fi
    else
        # Single browser mode
        run_tests
    fi
}

# ============================================================================
# SCRIPT ENTRY POINT
# ============================================================================
# Execute main function with all arguments
main "$@"