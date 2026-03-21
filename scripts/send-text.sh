#!/bin/bash
# Wrapper script for Python text generator
# Uses localhost and 45x35 geometry by default
# Uses 5x5.bdf font from ../flaschen-taschen/client/fonts/
# Runs from project code without requiring installation

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Calculate path to fonts directory
FONTS_DIR="$(dirname "$PROJECT_DIR")/flaschen-taschen/client/fonts"

# Add project directory to Python path so it can find flaschen_taschen
export PYTHONPATH="$PROJECT_DIR:$PYTHONPATH"

python -m flaschen_taschen.cli.send_text -g 45x35 -h localhost -f "$FONTS_DIR/5x5.bdf" "$@"
