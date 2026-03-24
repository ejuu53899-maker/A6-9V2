# Knowledge Base
- **NotebookLM**: [Access here](https://notebooklm.google.com/notebook/e8f4c29d-9aec-4d5f-8f51-2ca168687616)

# GenX FX Trading System [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A sophisticated trading automation framework integrating MQL5 Expert Advisors with Python for advanced analytics and execution.

The GenX FX Trading System is a curated collection of tools and scripts designed for traders who want to combine the power of MetaTrader 5 with the flexibility of Python-based data processing and signal generation.

## 🚀 Quick Start (V4)

### Prerequisites

- MetaTrader 5 (MT5) installed
- Python 3.8+
- `JULES_API_KEY_V4` (obtained from your dashboard)
- `GITHUB_TOKEN_PUSH` (for secure synchronization)

### Secret Environment Setup

For enhanced security, you can use an environment file to manage your keys.
1. Copy `GenX_FX_V4/.env.example` to `GenX_FX_V4/.env`.
2. Fill in your `JULES_API_KEY_V4` and `GITHUB_TOKEN_PUSH`.
3. The `startup.sh` script will automatically prioritize these variables.

### Installation

1. Clone this repository to your local machine.
2. Copy `GenX_FX_V4/GenX_EA_V4.mq5` to your MT5 `MQL5/Experts` folder.
3. Install Python dependencies:
   ```bash
   pip install -r GenX_FX_V4/requirements.txt
   ```

### Running

1. Compile and attach the EA in MT5, providing both `JULES_API_KEY_V4` and `GITHUB_TOKEN_PUSH`.
2. Start the Python bridge using the startup script:
   ```bash
   ./GenX_FX_V4/startup.sh "your_api_key_here" "your_github_token_here"
   ```

## 📁 Project Structure

```
GenX_FX/
├── GenX_FX_V4/
│   ├── GenX_EA_V4.mq5       # MQL5 Expert Advisor
│   ├── bridge.py            # Python Bridge (HTTP Server)
│   ├── startup.sh           # Easy Startup Script
│   └── requirements.txt     # Python Dependencies
├── Indexing-Workflow-controller/ # 🚀 Automated Signal Generation & Workflow Controller
├── signal_output/          # 📈 Generated Trading Signals (Excel, CSV, JSON)
├── README.md
└── ...
```

## 🚀 Indexing Workflow Integration (V4)

The system now features automated signal generation, an Excel-based dashboard, and **real-time performance monitoring**.

### **Real-Time Performance Monitoring**

Version 4 now tracks account performance metrics (balance, equity, pnl) and transmits them to the Python bridge for processing.
- **Endpoint:** `/performance/update`
- **Data:** Account number, balance, equity, and unrealized profit/loss.
- **Frequency:** Sent on initialization and every 500 ticks.

### **Remote Control Capabilities**

The Python bridge now acts as a command center for the EA.
- **POST `/remote/control`:** Send commands (`START`, `STOP`, `PAUSE`) to the bridge.
- **GET `/remote/status`:** The EA periodically checks this endpoint to sync its operational state.
- **State Persistence:** The bridge maintains the current status, allowing for remote intervention without restarting the EA.

### **Getting Started with Signals**

1. **Setup Environment:**
   ```bash
   pip install openpyxl pandas
   ```
2. **Generate Signals:**
   ```bash
   export PYTHONPATH=$PYTHONPATH:$(pwd)/Indexing-Workflow-controller/scripts/utils
   python3 Indexing-Workflow-controller/scripts/utils/demo_excel_generator.py
   ```
3. **View Outputs:**
   Check the `signal_output/` directory for the latest Excel dashboard and MT4/MT5 CSV signals.

### **Active Trading Session Entry**

To connect a remote MetaTrader 5 terminal to an active bridge session:
1. Ensure your firewall allows inbound connections on the configured bridge port (default: 8000).
2. In your MT5 Expert Advisor, set `BridgeURL` to the public IP or hostname of the bridge server (e.g., `http://your-server-ip:8000`).
3. Ensure the `JULES_API_KEY_V4` and `GITHUB_TOKEN_PUSH` in MT5 match the session tokens.

## 🧪 Testing

The project includes a suite of automated tests to ensure bridge functionality and security.
- **Python Bridge Syntax Check:** `python3 -m py_compile GenX_FX_V4/bridge.py`
- **Integration Test:** Verified via GitHub Actions using mock authentication tokens.

## 🚀 CI/CD & Deployment

The system is equipped with a GitHub Actions pipeline (`.github/workflows/ci-cd.yml`) that automates:
1. **Linting:** Checks Python code quality using Flake8.
2. **Testing:** Runs syntax and integration tests in a virtual environment.
3. **Security:** Performs filesystem vulnerability scans using Trivy.
4. **Building:** Packages the EA and Bridge into a versioned `.tar.gz` artifact.
5. **Deployment:** Automatically deploys to the `development` environment on every push to `main`. Production deployment is available via manual `workflow_dispatch`.

## 🏗️ Building

```bash
# Build based on project type
```



## 📝 Development

### Code Style

Follow project-specific style guidelines

### Contributing

1. Fork the repository
2. Create a feature branch (git checkout -b feature/amazing-feature)
3. Commit your changes (git commit -m 'Add amazing feature')
4. Push to the branch (git push origin feature/amazing-feature)
5. Open a Pull Request

## 🔧 Configuration





## 📄 License

[![CC0](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/cc-zero.svg)](https://creativecommons.org/publicdomain/zero/1.0/)

This project is licensed under the [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) (Public Domain Dedication).

## 👥 Authors

- Your Name

## 🙏 Acknowledgments

- Thanks to all contributors

---

**Last Updated:** 2026-01-16
