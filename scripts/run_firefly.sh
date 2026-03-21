#!/bin/bash
# Run firefly demo (wandering particles with trails)
cd "$(dirname "$0")/.."
python3 -m flaschen_taschen.demos.firefly -t 10 -p chase -d 100 -l 6 "$@"
