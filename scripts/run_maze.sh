#!/bin/bash
# Run maze demo (procedural maze generation using depth-first search)
cd "$(dirname "$0")/.."
python3 -m flaschen_taschen.demos.maze -d 20 -t 5 -l 5 "$@"
