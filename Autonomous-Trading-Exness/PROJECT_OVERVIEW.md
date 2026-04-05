# GenX FX - Project Overview

## 🌌 System Architecture

GenX FX is a sophisticated autonomous trading system designed for Exness MetaTrader 5 (MT5), integrating traditional technical analysis (SMC + Trend Breakout) with cutting-edge AI verification (Google Gemini & Jules AI).

### 1. 🌉 Trading Bridge (FastAPI)
The core orchestrator of the system.
- **Location**: `api/main.py`
- **Function**: Acts as a middleware between the MT5 Expert Advisors (EAs) and external execution/monitoring services.
- **Port**: 8080 (default)
- **API Endpoints**:
  - `/api/get_signals`: MT5 EA polls this to check for executable signals.
  - `/api/status`: Used to report execution status back to the bridge.

### 2. 📈 MT5 Integration (MQL5)
Proprietary indicators and EAs for the MT5 desktop platform.
- **Indicator**: `mt5/MQL5/Indicators/SMC_TrendBreakout_MTF.mq5` (BOS/CHoCH, Donchian Breakout, Multi-Timeframe confirmation).
- **Expert Advisor (EA)**: `mt5/MQL5/Experts/SMC_TrendBreakout_MTF_EA.mq5` (Automated execution, Risk Management, AI Filtering).

### 3. 🤖 AI Verification Layer
Before a trade is executed, it can be filtered through an AI model to increase probability.
- **Providers**: Google Gemini, Jules AI.
- **Implementation**: Integrated directly into the MQL5 EA via WebRequests.
- **Configuration**: API keys are stored in MT5 EA inputs or pulled from the secure vault.

### 4. ⚙️ Startup & Management
A suite of scripts to handle the lifecycle of the trading system.
- **`start.sh`**: Primary entry point to launch the Python orchestrator and API bridge.
- **`scripts/start_trading.py`**: Monitors signals and coordinates execution across Bybit (crypto) or MT5 (forex).
- **`scripts/echo_run.sh`**: Triggered by F12, ensures system state is extracted and the core logic is running.

### 5. 🚀 CI/CD & Deployment Pipeline
Automated workflows to keep the system updated and deployed.
- **GitHub Actions**: Workflows for CI (validation), CD (cloud deployment), and OneDrive Sync.
- **`scripts/pr_tool.py`**: Automated tool for pushing changes, creating Pull Requests, and merging to `main`.
- **`setup-github-secrets.sh`**: Syncs local `.env` variables to GitHub Repository Secrets for secure automation.

## 🛠️ Management Control

The system is designed for "Set and Forget" operation with centralized management:
- **Telegram Bot**: `scripts/telegram_deploy_bot.py` allows remote status checks and deployments.
- **Unified Setup**: `setup.sh` provides a menu-driven interface for full environment validation and tool installation.
- **Secure Vault**: `config/vault.json` (templated in `vault.json.template`) stores sensitive credentials away from the source code.

## 📦 Deployment Options
- **Docker**: `Dockerfile.production` and `docker-compose.production.yml` for containerized environments.
- **Cloud Platforms**: Integrated support for Render, Railway, Fly.io, and **Google Cloud Platform (App Engine/Cloud Run)**.
- **VPS**: Targeted deployment to Ubuntu 22.04 LTS via GitHub Actions.

---
*GenX FX: Empowering Sovereignty through Autonomous Trading.*
