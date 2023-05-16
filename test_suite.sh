#!/bin/bash
# This script runs the three Python scripts in the test suite
# Store the arguments passed to the shell script

# Usage: ./test_suite.sh <domain_name> [path] <iterations>
args="$@"
domain_name=$1
iterations=$3

# Check if the second argument is empty
if [ ! -z "$2" ]; then
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

