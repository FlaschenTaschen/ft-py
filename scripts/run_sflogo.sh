#!/bin/bash
# Run sflogo demo (bouncing SF tree logo)
cd "$(dirname "$0")/.."
python3 -m flaschen_taschen.demos.sflogo -d 50 -t 30 -l 5 "$@"
