#!/bin/bash
# This script runs the three Python scripts in the test suite
# Store the arguments passed to the shell script

# Usage: ./test_suite.sh <domain_name> [path] <iterations>
args="$@"
domain_name=$1
iterations=$3
args="$@"

# Iterate through the arguments
for arg in $args; do
    # Check if the argument is '-help'
    if [[ "$arg" == "--help" || "$arg" == "-h" ]]; then
        # Display help information
        echo "Help information:"
        echo "Usage: ./test_suite.sh <domain_name> [path] <iterations>"
        echo "- <domain_name>: The domain name of the AS to test (e.g. 17-ffaa:1:1063)"
        echo "- [path]: The pre-selected path to enter in interactive mode (it is an integer). This is optional."
        echo "- <iterations>: The number of iterations for which each script needs to be run (as an integer)"        

        exit 0
    fi
done

# Check if the second argument is empty
if [ -z "$2" ]; then
    echo "Running latency test with no path..."
    python3 Tests/latency_test.py -d "$domain_name" -n "$iterations"
    exit 1
else 
    path=$2
    python3 Tests/latency_test.py -d "$domain_name" -i "$path" -n "$iterations"
fi


# # Add commands to run each Python script, passing the stored arguments
# python bw_test.py $args
# python loss_test.py $args

