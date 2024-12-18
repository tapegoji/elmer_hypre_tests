#!/bin/bash

set -euo pipefail

# Default mesh file
MESH_FILE="case.msh"

# Default number of processes (all available cores minus one)
DEFAULT_NUM_PROCS=$(( $(nproc) - 1 ))
NUM_PROCS="$DEFAULT_NUM_PROCS"

# Function to display usage instructions
usage() {
    echo "Usage: $0 [-parallel [NUM_PROCS]] [-mesh MESH_FILE]"
    exit 1
}

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
        -mesh)
            shift
            if [[ $# -eq 0 ]]; then
                echo "Error: -mesh requires a file argument."
                usage
            fi
            MESH_FILE="$1"
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

# Run ElmerGrid based on the mode
if [[ $PARALLEL_MODE -eq 1 ]]; then
    echo "Running ElmerGrid in parallel mode with $NUM_PROCS processes"
    ElmerGrid 14 2 "$MESH_FILE" -partdual -metiskway "$NUM_PROCS" -autoclean
else
    echo "Running ElmerGrid in serial mode"
    ElmerGrid 14 2 "$MESH_FILE" -autoclean
fi
