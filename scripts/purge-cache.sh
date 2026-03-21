#!/bin/bash
# Purge Python bytecode cache and __pycache__ directories
# This ensures Python reloads all modules fresh on next run

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Purging Python cache in $REPO_ROOT..."

# Remove all __pycache__ directories
find "$REPO_ROOT" -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

# Remove all .pyc files
find "$REPO_ROOT" -name "*.pyc" -delete 2>/dev/null || true

# Remove pytest cache
rm -rf "$REPO_ROOT/.pytest_cache" 2>/dev/null || true

# Remove .egg-info directories
find "$REPO_ROOT" -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

echo "✓ Cache purged successfully"
