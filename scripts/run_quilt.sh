#!/bin/bash
# Run quilt demo (procedural quilt pattern)
cd "$(dirname "$0")/.."
python3 -m flaschen_taschen.demos.quilt -t 15 -l 7 -d 100 "$@"
