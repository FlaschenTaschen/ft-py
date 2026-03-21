#!/bin/bash
# Debugger script - cycles through colors while drawing edges or filling display
# Usage: ./debugger.sh -m edges [-t 10] [-d 0] [--palette rainbow]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

export PYTHONPATH="$PROJECT_DIR:$PYTHONPATH"

python -m flaschen_taschen.cli.ft_debugger -m edges "$@"
