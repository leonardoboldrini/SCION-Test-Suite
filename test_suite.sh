#!/bin/bash#
# This script runs the entire test suite
# Store the arguments passed to the shell script

# Usage: ./test_suite.sh <iterations>
iterations=$1
args="$@"

display_help_info() {
    echo "Help information:"
    echo "Usage: ./test_suite.sh <iterations>"
    echo "Arguments:"
    echo "  -h, --help: Display help information"
    echo "  <iterations>: Number of iterations to run the test suite"
}

# Iterate through the arguments
for arg in $args; do
    # Check if the argument is '-help'
    if [[ "$arg" == "--help" || "$arg" == "-h" ]]; then
        # Display help information
        display_help_info
        exit 0
    fi
done

if [ -z "$iterations" ]; then
    echo "Please provide the iterations number as an argument."
    # Display help information
    display_help_info
    exit 1
fi
# Check if the second argument is empty
echo "Collecting all the paths..."
python3 collect_paths.py

echo "Running the test suite..."
exit 1


# # Add commands to run each Python script, passing the stored arguments
# python bw_test.py $args
# python loss_test.py $args

#let's see
