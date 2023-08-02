#!/bin/bash
# This script runs the entire test suite
# Store the arguments passed to the shell script

# Usage: ./test_suite.sh <iterations>
iterations=$1
args="$@"


# Collect the paths
echo "Collecting all the paths..."
python3 ../collect_paths.py

echo "Running the bw test suite..."
python3 bw_temp_test.py -n $1
exit 0

