#!/bin/bash
# Run black demo (clear display to black)
cd "$(dirname "$0")/.."
python3 -m flaschen_taschen.demos.black "$@"
