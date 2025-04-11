#!/usr/bin/env python3
"""
Script to run a specific test multiple times with proper reporting.
Usage: python run_multiple_times.py
"""

import argparse
import glob
import os
import subprocess
import sys
import time
from datetime import datetime


def run_test_multiple_times(test_path, iterations=100, allure_dir="allure-results"):
    """
    Run a specific test multiple times with allure reporting.

    Args:
        test_path: Path to the test (e.g., 'tests/test_end_to_end.py::test_swag_checkout_end_to_end')
        iterations: Number of times to run the test
        allure_dir: Directory for Allure results

    Returns:
        tuple: (passed_count, failed_count, results)
    """
    # Create results directory if it doesn't exist
    if not os.path.exists(allure_dir):
        os.makedirs(allure_dir)

    # Clean previous results to avoid confusion
    for item in glob.glob(f"{allure_dir}/*"):
        if os.path.isdir(item):
            for file in glob.glob(f"{item}/*"):
                os.remove(file)
            os.rmdir(item)
        else:
            os.remove(item)

    start_time = time.time()
    passed = 0
    failed = 0
    results = []

    print(f"Starting execution of {test_path} {iterations} times...")
    print(f"Tests will run with Allure reporting to {allure_dir}")
    print("-" * 80)

    for i in range(iterations):
        iteration_start = time.time()
        print(f"Running iteration {i + 1}/{iterations}...")

        # Create a unique subfolder for each test run to prevent overwrites
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        iteration_dir = f"{allure_dir}/run_{i + 1}_{timestamp}"
        os.makedirs(iteration_dir, exist_ok=True)

        # Build the pytest command
        cmd = [
            "pytest",
            test_path,
            "-v",
            f"--alluredir={iteration_dir}"
        ]

        # Run the test
        result = subprocess.run(cmd, capture_output=True, text=True)

        # Process the result
        duration = time.time() - iteration_start
        status = "PASSED" if result.returncode == 0 else "FAILED"
        if status == "PASSED":
            passed += 1
        else:
            failed += 1

        results.append({
            "iteration": i + 1,
            "status": status,
            "duration": duration,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "allure_dir": iteration_dir
        })

        # Print status
        print(f"Iteration {i + 1}: {status} (took {duration:.2f}s)")
        if status == "FAILED":
            print("ERROR OUTPUT:")
            print(result.stderr)
            print("-" * 40)

        # Give the system a moment to clean up resources
        time.sleep(1)

    # Calculate statistics
    total_duration = time.time() - start_time
    pass_rate = (passed / iterations) * 100 if iterations > 0 else 0

    # Print summary
    print("\n" + "=" * 80)
    print(f"EXECUTION SUMMARY:")
    print(f"Total iterations: {iterations}")
    print(f"Passed: {passed} ({pass_rate:.2f}%)")
    print(f"Failed: {failed} ({100 - pass_rate:.2f}%)")
    print(f"Total duration: {total_duration:.2f}s")
    print(f"Average test duration: {total_duration / iterations:.2f}s if iterations > 0 else 0")
    print("=" * 80)

    return passed, failed, results


def main():
    parser = argparse.ArgumentParser(description='Run a test multiple times with Allure reporting')
    parser.add_argument('--test', default='tests/test_end_to_end.py::test_swag_end_to_end',
                        help='Test path (default: tests/test_end_to_end.py::test_swag_end_to_end)')
    parser.add_argument('--iterations', type=int, default=100,
                        help='Number of iterations (default: 100)')
    parser.add_argument('--allure-dir', default='allure-results',
                        help='Allure results directory (default: allure-results)')
    parser.add_argument('--generate-report', action='store_true',
                        help='Generate Allure report after completion')
    parser.add_argument('--clean', action='store_true',
                        help='Clean results directory before running')

    args = parser.parse_args()

    # Run the test multiple times
    passed, failed, results = run_test_multiple_times(
        args.test, args.iterations, args.allure_dir
    )

    # Generate Allure report if requested
    if args.generate_report:
        print("\nGenerating Allure report...")

        # Generate a timestamp for the report directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_dir = f"allure-report-{timestamp}"

        # Combine all run directories when generating the report
        run_dirs = [result["allure_dir"] for result in results]

        # For MacOS/Linux
        all_dirs = " ".join(run_dirs)
        os.system(f'allure generate {all_dirs} -o {report_dir} --clean')

        print(f"Report generated in {report_dir} directory")

        # Try to open the report automatically
        try:
            if sys.platform == "darwin":  # macOS
                os.system(f"open {report_dir}/index.html")
            elif sys.platform == "win32":  # Windows
                os.system(f"start {report_dir}/index.html")
            elif sys.platform.startswith("linux"):  # Linux
                os.system(f"xdg-open {report_dir}/index.html")
        except Exception as e:
            print(f"Could not open report automatically: {e}")
            print(f"Please open {report_dir}/index.html manually")

    # Return non-zero exit code if any test failed
    return 1 if failed > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
