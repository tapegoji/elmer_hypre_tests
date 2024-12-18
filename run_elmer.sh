#!/bin/bash

set -euo pipefail

# Default case file
CASE_FILE="case.sif"

# Default number of processes (all available cores minus one)
DEFAULT_NUM_PROCS=$(( $(nproc) - 1 ))
NUM_PROCS="$DEFAULT_NUM_PROCS"

# Function to display usage instructions
usage() {
    echo "Usage: $0 [-parallel [NUM_PROCS]] [-case CASE_FILE]"
    exit 1
}

# Clean up previous results and directories
[ -d "results" ] && rm -rf results/*
[ -d "precice-run" ] && rm -rf precice-run
mkdir -p results

# Initialize variables
PARALLEL_MODE=0

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -parallel)
            PARALLEL_MODE=1
            shift
            if [[ $# -gt 0 ]] && [[ ! "$1" =~ ^- ]]; then
                NUM_PROCS="$1"
                shift
            fi
            ;;
        -case)
            shift
            if [[ $# -eq 0 ]]; then
                echo "Error: -case requires a file argument."
                usage
            fi
            CASE_FILE="$1"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done

# Validate NUM_PROCS if in parallel mode
if [[ $PARALLEL_MODE -eq 1 ]]; then
    if ! [[ "$NUM_PROCS" =~ ^[0-9]+$ ]] || [[ "$NUM_PROCS" -le 0 ]]; then
        echo "Error: Number of processes must be a positive integer."
        usage
    fi
fi

# Run ElmerSolver based on the mode
if [[ $PARALLEL_MODE -eq 1 ]]; then
    echo "Running ElmerSolver in parallel mode with $NUM_PROCS processes"
    mpirun -np "$NUM_PROCS" --oversubscribe -v ElmerSolver_mpi "$CASE_FILE"
else
    echo "Running ElmerSolver in serial mode"
    ElmerSolver "$CASE_FILE"
fi

# Launch Paraview in the background
paraview &
