# Next-Forge (forge.mql5.io) Act Runner Setup

This guide describes how to set up an Act Runner for the **forge.mql5.io** Gitea instance to enable CI/CD on your VPS.

## 1. Prerequisites
- Docker installed and running on your VPS.
- Access to your repository settings on `https://forge.mql5.io/LengKundee/mql5`.

## 2. Obtain Registration Token
1. Log in to `https://forge.mql5.io`.
2. Navigate to your repository: `LengKundee/mql5`.
3. Go to **Settings** -> **Actions** -> **Runners**.
4. Click **'Create new Runner'** and copy the **Registration Token**.

## 3. Launch the Setup Script
On your VPS, execute the provided setup script:

```bash
# Navigate to the desktop_mode_repo configuration
cd desktop_mode_repo/vps-config

# Run the setup script (ensure you have the token ready)
REGISTRATION_TOKEN="your_token_here" ./setup_runner.sh
```

## 4. Verify Runner Status
After the script completes, the runner will be registered and started as a systemd service.

```bash
# Check service status
sudo systemctl status act_runner

# Check runner logs
journalctl -u act_runner -f
```

## 5. Enable Actions in Repository
Ensure Actions are enabled in your repository settings on `forge.mql5.io` so the runner can start picking up jobs from `.github/workflows/`.
