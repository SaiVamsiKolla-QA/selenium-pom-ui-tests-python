#!/bin/bash
echo "Running Swag Labs Tests with Allure Reporting"

# Run the cleanup script first
python cleanup.py

# Create results directory if it doesn't exist (clean run)
if [ -d "allure-results" ]; then
    echo "Cleaning previous results..."
    rm -rf allure-results
fi
mkdir -p allure-results

# Set number of iterations
ITERATIONS=1

# Run the tests multiple times
for (( i=1; i<=$ITERATIONS; i++ ))
do
    echo "========================================"
    echo "Running test iteration $i of $ITERATIONS"
    echo "========================================"

    # Run the tests with Allure reporting
    echo "Running tests..."
    pytest tests/ -v --alluredir=allure-results

    echo "Iteration $i completed."
    echo ""
done

# Generate and open the Allure report
echo "Generating Allure report..."
allure serve allure-results

echo "Test execution completed."