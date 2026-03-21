#!/bin/bash
# Run plasma demo (smooth plasma with color cycling)
cd "$(dirname "$0")/.."
python3 -m flaschen_taschen.demos.plasma "$@"
