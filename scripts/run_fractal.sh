#!/bin/bash
# Run fractal demo (Mandelbrot set with smooth zoom animation)
cd "$(dirname "$0")/.."
python3 -m flaschen_taschen.demos.fractal -d 50 -t 30 -l 5 "$@"
