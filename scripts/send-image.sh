#!/bin/bash
# Wrapper script for Python image generator
# Uses localhost and 45x35 geometry by default
# Runs from project code without requiring installation

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Add project directory to Python path so it can find flaschen_taschen
export PYTHONPATH="$PROJECT_DIR:$PYTHONPATH"

python -m flaschen_taschen.cli.send_image -g 45x35 -h localhost -t 5 "$@"
