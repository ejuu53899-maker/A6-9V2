# Knowledge Base
- **NotebookLM**: [Access here](https://notebooklm.google.com/notebook/e8f4c29d-9aec-4d5f-8f51-2ca168687616)

# GenX FX Trading System

## 📋 Description

A sophisticated trading automation framework integrating MQL5 Expert Advisors with Python for advanced analytics and execution.

## 🚀 Quick Start (V4)

### Prerequisites

- MetaTrader 5 (MT5) installed
- Python 3.8+
- `JULES_API_KEY_V4` (obtained from your dashboard)
- `GITHUB_TOKEN_PUSH` (for secure synchronization)

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
├── README.md
└── ...
```

## 🧪 Testing

```bash
# Run tests based on project type
```

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

See LICENSE file for details.

## 👥 Authors

- Your Name

## 🙏 Acknowledgments

- Thanks to all contributors

---

**Last Updated:** 2026-01-16
