#!/usr/bin/env python3
import argparse
import os
import statistics
import subprocess
import time
from datetime import datetime


def create_directories():
    """Create necessary directories for logs and reports"""
    os.makedirs("logs", exist_ok=True)
    os.makedirs("reports", exist_ok=True)


def run_test(test_path, iterations=1, report=True):
    """
    Run a specified test multiple times

    Args:
        test_path: Path to the test file with optional test case (e.g. tests/test_login.py::test_swag_login)
        iterations: Number of times to run the test
        report: Whether to generate Allure reports
    """
    create_directories()

    # Parse the test path to get a meaningful name for the log file
    test_name = test_path.split("/")[-1]
    if "::" in test_name:
        test_name = test_name.split("::")[-1]
    else:
        test_name = test_name.replace(".py", "")

    # Create a timestamp for the log file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"logs/{test_name}_{timestamp}.log"

    # Open the log file
    with open(log_file, "w") as log:
        log.write(f"Starting test run: {test_path}\n")
        log.write(f"Iterations: {iterations}\n")
        log.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log.write("=" * 80 + "\n\n")

        successes = 0
        failures = 0
        durations = []

        for i in range(1, iterations + 1):
            log.write(f"\nRun #{i} of {iterations} - {datetime.now().strftime('%H:%M:%S')}\n")
            log.write("-" * 50 + "\n")

            # Construct the pytest command
            cmd = ["pytest", test_path, "-v"]
            if report:
                cmd.extend(["--alluredir=allure-results"])

            # Run the test
            start_time = time.time()
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate()
            end_time = time.time()

            # Calculate duration
            duration = end_time - start_time
            durations.append(duration)

            # Write output to log
            log.write(f"STDOUT:\n{stdout}\n")
            if stderr:
                log.write(f"STDERR:\n{stderr}\n")

            # Determine if the test passed
            if process.returncode == 0:
                result = "PASSED"
                successes += 1
            else:
                result = "FAILED"
                failures += 1

            # Write result and time
            log.write(f"Result: {result}\n")
            log.write(f"Duration: {duration:.2f} seconds\n")
            log.write("-" * 50 + "\n")

            # Print progress to console
            print(f"Run {i}/{iterations}: {result} in {duration:.2f}s")

        # Calculate statistics
        avg_duration = sum(durations) / len(durations)
        min_duration = min(durations)
        max_duration = max(durations)
        std_dev = statistics.stdev(durations) if len(durations) > 1 else 0

        # Write summary
        log.write("\nSUMMARY\n")
        log.write("=" * 50 + "\n")
        log.write(f"Total runs: {iterations}\n")
        log.write(f"Passed: {successes}\n")
        log.write(f"Failed: {failures}\n")
        log.write(f"Success rate: {(successes / iterations) * 100:.2f}%\n")
        log.write(f"\nPerformance metrics:\n")
        log.write(f"Average run time: {avg_duration:.2f} seconds\n")
        log.write(f"Minimum run time: {min_duration:.2f} seconds\n")
        log.write(f"Maximum run time: {max_duration:.2f} seconds\n")
        log.write(f"Standard deviation: {std_dev:.2f} seconds\n")

        # Print summary to console
        print("\nTest Run Complete!")
        print(f"Results: {successes} passed, {failures} failed")
        print(f"Success rate: {(successes / iterations) * 100:.2f}%")
        print(f"Average run time: {avg_duration:.2f} seconds")
        print(f"Min: {min_duration:.2f}s, Max: {max_duration:.2f}s, StdDev: {std_dev:.2f}s")
        print(f"Log file: {log_file}")

        # Generate Allure report if requested
        if report:
            try:
                report_dir = f"reports/{test_name}_{timestamp}"
                os.makedirs(report_dir, exist_ok=True)
                subprocess.run(["allure", "generate", "allure-results", "-o", report_dir, "--clean"])
                print(f"Allure report generated in: {report_dir}")
            except Exception as e:
                print(f"Warning: Could not generate Allure report: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description="Run automated tests multiple times")
    parser.add_argument(
        "test_path",
        help="Path to the test file or test case (e.g., tests/test_login.py or tests/test_login.py::test_swag_login)"
    )
    parser.add_argument(
        "-n", "--iterations",
        type=int,
        default=1,
        help="Number of times to run the test (default: 1)"
    )
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Disable Allure report generation"
    )

    args = parser.parse_args()

    run_test(args.test_path, args.iterations, not args.no_report)


if __name__ == "__main__":
    main()