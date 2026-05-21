#!/bin/bash

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="$REPO_ROOT/dist"
PACKAGE_NAME="Exness_MT5_MQL5.zip"

echo "Packaging MT5 files..."
mkdir -p "$DIST_DIR"

if [ -d "$REPO_ROOT/mt5/MQL5" ]; then
    cd "$REPO_ROOT/mt5"
    zip -r "$DIST_DIR/$PACKAGE_NAME" MQL5
    echo "Package created at dist/$PACKAGE_NAME"
else
    echo "Error: mt5/MQL5 directory not found."
fi
