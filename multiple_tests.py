#!/usr/bin/env python3
import argparse
import os
import subprocess
import statistics
import time
from datetime import datetime


def run_test(test_path, iterations=1, report=True, browser="chrome", parallel_workers=None):
    """
    Run a specified test multiple times
    """
    # Create browser-specific results directory
    results_dir = f"allure-results/{browser}"
    os.makedirs(results_dir, exist_ok=True)

    print(f"Running {test_path} with browser: {browser}")
    print(f"Iterations: {iterations}")
    print(f"Parallel Workers: {parallel_workers if parallel_workers else 'None (Sequential)'}")

    successes = 0
    failures = 0
    durations = []

    for i in range(1, iterations + 1):
        # Construct the pytest command
        cmd = ["pytest", test_path, "-v", "--browser", browser]

        # Add parallel execution if requested
        if parallel_workers:
            cmd.extend(["-n", str(parallel_workers)])

        if report:
            cmd.extend(["--alluredir", results_dir])

        # Run the test
        start_time = time.time()
        process = subprocess.run(cmd, capture_output=True, text=True)
        end_time = time.time()

        # Calculate duration
        duration = end_time - start_time
        durations.append(duration)

        # Determine if the test passed
        if process.returncode == 0:
            result = "PASSED"
            successes += 1
        else:
            result = "FAILED"
            failures += 1

        # Print progress to console
        print(f"Run {i}/{iterations} ({browser}): {result} in {duration:.2f}s")

    # Calculate statistics
    avg_duration = sum(durations) / len(durations)
    min_duration = min(durations)
    max_duration = max(durations)
    std_dev = statistics.stdev(durations) if len(durations) > 1 else 0

    # Print summary to console
    print("\nTest Run Complete!")
    print(f"Browser: {browser}")
    print(f"Results: {successes} passed, {failures} failed")
    print(f"Success rate: {(successes / iterations) * 100:.2f}%")
    print(f"Average run time: {avg_duration:.2f} seconds")
    print(f"Min: {min_duration:.2f}s, Max: {max_duration:.2f}s, StdDev: {std_dev:.2f}s")

    # Generate Allure report if requested
    if report:
        try:
            report_dir = f"reports/{browser}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.makedirs(report_dir, exist_ok=True)
            subprocess.run(["allure", "generate", results_dir, "-o", report_dir, "--clean"])
            print(f"Allure report generated in: {report_dir}")
        except Exception as e:
            print(f"Warning: Could not generate Allure report: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description="Run automated tests multiple times")
    parser.add_argument(
        "test_path",
        help="Path to the test file or test case (e.g., Tests/test_login.py or Tests/test_login.py::test_swag_login)"
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
    parser.add_argument(
        "--browser",
        default="chrome",
        help="Browser to run tests with (chrome, firefox, edge, safari)"
    )
    parser.add_argument(
        "--parallel",
        type=int,
        help="Number of parallel workers to use with pytest-xdist"
    )

    args = parser.parse_args()

    run_test(
        args.test_path,
        args.iterations,
        not args.no_report,
        args.browser,
        args.parallel
    )


if __name__ == "__main__":
    main()