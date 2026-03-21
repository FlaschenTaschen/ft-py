#!/bin/bash
# Run blur demo (Gaussian blur effect)
cd "$(dirname "$0")/.."
python3 -m flaschen_taschen.demos.blur -d 100 -l 5 -t 5 -p 2 target "$@"
