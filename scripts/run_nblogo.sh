#!/bin/bash
# Run nblogo demo (bouncing Noisebridge logo)
cd "$(dirname "$0")/.."
python3 -m flaschen_taschen.demos.nblogo -d 50 -t 30 -l 5 "$@"
