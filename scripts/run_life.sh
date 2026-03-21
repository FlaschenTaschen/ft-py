#!/bin/bash
# Run life demo (Conway's Game of Life cellular automaton)
cd "$(dirname "$0")/.."
python3 -m flaschen_taschen.demos.life -t 5 -d 200 -n 6 -l 5 "$@"
