#!/bin/bash
# Run simple animation demo (moving circles with sine motion)
cd "$(dirname "$0")/.."
python3 -m flaschen_taschen.demos.simple_animation -t 15 -d 20 -l 6 "$@"
