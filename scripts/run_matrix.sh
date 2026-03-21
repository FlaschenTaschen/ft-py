#!/bin/bash
# Run matrix demo (matrix-style falling characters)
cd "$(dirname "$0")/.."
python3 -m flaschen_taschen.demos.matrix -d 100 -t 5 -l 5 "$@"
