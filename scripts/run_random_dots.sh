#!/bin/bash
# Run random dots demo (random colored dots at random positions)
cd "$(dirname "$0")/.."
python3 -m flaschen_taschen.demos.random_dots -d 50 -t 30 -l 5 "$@"
