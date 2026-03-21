#!/bin/bash
# Run simple example demo (static colored rectangles)
cd "$(dirname "$0")/.."
python3 -m flaschen_taschen.demos.simple_example -t 5 -l 6 "$@"
