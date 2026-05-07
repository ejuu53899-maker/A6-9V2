#!/bin/bash

# Production Deployment Script for Hostinger VPS
# Target: exness-mt5real24.net (187.77.140.66)

VPS_IP="187.77.140.66"
REMOTE_USER="root"
DEPLOY_DIR="/app/trading_system"

echo "=========================================="
echo "   GenX VPS Production Deployment         "
echo "=========================================="

# Check for SSH access
if ! ssh -o ConnectTimeout=5 -o BatchMode=yes $REMOTE_USER@$VPS_IP exit &>/dev/null; then
    echo "[ERROR] Cannot reach VPS via SSH. Ensure your key is added and VPS is up."
    exit 1
fi

echo "[1/3] Syncing files to VPS..."
rsync -avz --exclude='.git' --exclude='node_modules' --exclude='__pycache__' ./ $REMOTE_USER@$VPS_IP:$DEPLOY_DIR

echo "[2/3] Preparing Environment on VPS..."
# Ensure the .env file exists or is updated on the VPS
ssh $REMOTE_USER@$VPS_IP "cd $DEPLOY_DIR && [ ! -f .env ] && cp GenX_FX_V4/.env.fxpro .env || echo '.env already exists'"

echo "[3/3] Starting Services via Docker Compose..."
ssh $REMOTE_USER@$VPS_IP "cd $DEPLOY_DIR && docker compose up -d --build"

echo "=========================================="
echo "   Deployment to $VPS_IP Complete        "
echo "=========================================="
