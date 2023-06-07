#!/bin/bash
# This script runs the entire test suite
# Store the arguments passed to the shell script

# Usage: ./test_suite.sh <iterations>
iterations=$1
args="$@"

display_help_info() {
    echo "Help information:"
    echo "Usage: ./test_suite.sh <iterations> [options]"
    echo "Arguments:"
    echo "  -h, --help: Display help information"
    echo "  <iterations>: Number of iterations to run the test suite"
    echo " --skip: Skip the path collection and run the test suite (optional but if present, MUST BE after <iterations>)"
    echo " --some_only: With this, the test suite will be run for maximu 2 paths for each destination (optional but if present, MUST BE after <iterations>)"
}

# Iterate through the arguments
for arg in $args; do
    # Check if the argument is '--help'
    if [[ "$arg" == "--help" || "$arg" == "-h" ]]; then
        # Display help information
        display_help_info
        exit 0
    fi
done

if ! [[ $1 =~ ^[0-9]+$ ]]; then
    echo "Invalid iterations argument. Argument is not a digit."
    display_help_info
else
    if [ -z "$iterations" ]; then
        echo "Please provide the iterations number as an argument."
        # Display help information
        display_help_info
        exit 1
    fi

    for arg in $args; do
        # Check if the argument is '--skip'
        if [[ "$arg" == "--skip" ]]; then
            echo "Skipping the path collection..."
            for arg in $args; do
                # Check if the argument is '--some_only'
                if [[ "$arg" == "--some_only" ]]; then
                    echo "Running the test suite for maximum 2 paths for each destination..."
                    python3 Tests/run_test.py -n $1 --some_only
                    exit 0
                fi
            done
            echo "Running the test suite..."
            python3 Tests/run_test.py -n $1
            exit 0
        fi
    done  

    # Collect the paths
    echo "Collecting all the paths..."
    python3 collect_paths.py

    for arg in $args: do
        # Check if the argument is '--some_only'
        if [[ "$arg" == "--some_only" ]]; then
            echo "Running the test suite for maximum 2 paths for each destination..."
            python3 Tests/run_test.py -n $1 --some_only
            exit 0
        fi
    done

    echo "Running the test suite..."
    python3 Tests/run_test.py -n $1
    exit 0
fi
