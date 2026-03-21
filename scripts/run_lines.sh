#!/bin/bash
# Run lines demo (random line animation with smooth color transitions)
cd "$(dirname "$0")/.."
python3 -m flaschen_taschen.demos.lines -d 200 -t 30 -l 5 -t 15 "$@"
