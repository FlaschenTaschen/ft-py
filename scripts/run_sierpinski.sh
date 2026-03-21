#!/bin/bash
# Run sierpinski demo (Sierpinski's Triangle fractal using chaos game algorithm)
cd "$(dirname "$0")/.."
python3 -m flaschen_taschen.demos.sierpinski -d 50 -t 30 -l 5 "$@"
