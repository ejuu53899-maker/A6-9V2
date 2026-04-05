# Hostinger VPS Deployment Guide (SSH Ed25519)

## 🚀 Overview
This project is configured for automated deployment to Hostinger VPS using GitHub Actions.

## 🛠️ Prerequisites
1.  **Hostinger VPS (Ubuntu 22.04 LTS)** at `34.46.237.233`.
2.  **SSH Ed25519 Private Key**: Ensure you have the private key corresponding to the public key:
    `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICw9/G//98IiSdsfAyn2tYS0ip9rE5wB6UAV1iue4dFm genxapitrading@gmail.com`
3.  **Docker & Docker Compose**: Installed on the VPS.

## 🔑 GitHub Secrets Configuration
Navigate to `Settings > Secrets and variables > Actions` in your GitHub repository and add:

| Secret Name | Value |
| :--- | :--- |
| `VPS_HOST` | `34.46.237.233` |
| `VPS_USERNAME` | `root` (or your specialized user) |
| `VPS_SSH_KEY` | Paste the **ENTIRE** content of your private key file (`id_ed25519`) |
| `VPS_PORT` | `22` |
| `DOCKER_USERNAME` | Your Docker Hub username |
| `DOCKER_TOKEN` | Your Docker Hub Personal Access Token |
| `TELEGRAM_TOKEN` | Your bot token from @BotFather |
| `TELEGRAM_CHAT_ID` | Your Telegram Chat ID |

## 🚢 Deployment Procedure
1.  **Push to `main`**: Any push to the `main` or `master` branch will trigger the `build-and-deploy` workflow.
2.  **Manual Dispatch**: You can manually trigger the deployment from the `Actions` tab on GitHub.
3.  **Monitor Logs**: Check the GitHub Actions logs for real-time status and health check results.

## 🧪 Post-Deployment
The system will:
1.  Build a new Docker image with TA-Lib support.
2.  Push to Docker Hub.
3.  SSH into the Hostinger VPS.
4.  Pull the latest `docker-compose.production.yml`.
5.  Start the Python API, Node.js server, and PostgreSQL/MongoDB/Redis databases.
6.  Perform a health check on `http://localhost:8000/health`.
7.  Notify you via Telegram.
