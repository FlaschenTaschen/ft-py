#!/bin/bash
# Run hack demo (rotating 3D text)
cd "$(dirname "$0")/.."
python3 -m flaschen_taschen.demos.hack -d 50 -t 30 -l 5 HACK "$@"
