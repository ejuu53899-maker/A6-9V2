#!/bin/bash
TARGET_DIR=$1

if [ -z "$TARGET_DIR" ]; then
    echo "Usage: ./scripts/deploy_mt5.sh <TARGET_DIR>"
else
    echo "Deploying MT5 files to $TARGET_DIR..."
    cp -rv mt5/MQL5/* "$TARGET_DIR/"
    echo "Deployment complete."
fi
