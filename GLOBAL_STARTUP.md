# Global Startup & Collaboration Guide

This guide is for all agents, collaborators, and sessions to quickly synchronize and start up the GenX Trading Environment on any device, including optimized support for **Mini PCs**.

## 🚀 Unified Startup Command

To start the entire system (Infrastructure + Trading Bridge) from any device:

```bash
./start_all.sh [JULES_API_KEY] [GITHUB_TOKEN] [go|python]
```

## 💻 Device-Specific Guides

### 1. Mini PC / Low Resource Devices
The system is optimized for devices with as little as 1GB RAM.
- Use the **Go Bridge** (`go`) for maximum performance and minimal memory footprint.
- The `start_all.sh` script automatically detects low-resource environments and applies passive optimizations.

### 2. Desktop / Cloud Servers
- You can host the **Forgejo/Gitea** service locally using the provided `docker-compose.yml`.
- Access your local git server at `http://localhost:3001`.

### 3. Development / Debugging
- Use the **Python Bridge** (`python`) if you need to quickly modify the bridge logic without recompiling.

## 🤝 Collaboration Protocol

1. **Pull Latest Changes**: Ensure you have the latest code and submodule state:
   ```bash
   git pull --recurse-submodules
   git submodule update --init --recursive
   ```
2. **Set Credentials**: Export your keys globally or provide them to the `start_all.sh` script.
3. **Bridge Communication**: The MQL5 EA connects to the bridge on **port 8000** by default. Ensure your firewall allows local traffic on this port.

## 🌍 Live Production Environment

- **Domain**: `exness-mt5real24.net`
- **VPS IP**: `187.77.140.66` (Malaysia - Kuala Lumpur)
- **Status**: DNS configured via `scripts/setup_hostinger_dns.py`
- **Access**: Managed via `deploy_vps.sh` for automated production pushes.

## 🏗️ System Components
- **Go Bridge**: `GenX_Go_Bridge/` (High Performance)
- **Python Bridge**: `GenX_FX_V4/` (Flexible)
- **EA**: `GenX_FX_V4/GenX_EA_V4.mq5`
- **Infrastructure**: Root `docker-compose.yml` (Forgejo/Gitea + Postgres)

---
**Tag**: @all-agents @collaborators - Let's start the session together!
