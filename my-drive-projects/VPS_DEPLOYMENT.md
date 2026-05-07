# MetaTrader VPS Deployment Guide - FxPro Real MT5

This guide describes how to deploy the GenX EA V4 to the MetaTrader VPS for use with an FxPro Real MT5 Standard account.

## 📋 Prerequisites

1.  **FxPro MT5 Account**: Ensure you have a "Real MT5 Standard" account active with FxPro.
2.  **MetaTrader VPS Subscription**: Activate the built-in MQL5 VPS from within your MT5 terminal.
3.  **Bridge Server**: Ensure your Bridge (Python or Go) is running on `WIN-DNGG6AODSKQ` (via WSL2) and is accessible via a public URL (e.g., via `ngrok` or a fixed IP if hosted on a cloud VPS).

## 🚀 Deployment Steps

### 1. Configure the EA
Open `GenX_EA_V4.mq5` in MetaEditor and set the following input parameters:
*   `JULES_API_KEY_V4`: Your secure token.
*   `BridgeURL`: The public URL of your bridge server (Required for VPS).
    *   *Note: `localhost` will not work on MetaTrader VPS.*

### 2. Prepare the MT5 Terminal
1.  Log in to your FxPro Real account in the MT5 terminal on `WIN-DNGG6AODSKQ`.
2.  Open the desired charts and attach `GenX_EA_V4` to them.
3.  Ensure "Algo Trading" is enabled in the terminal.
4.  Add your Bridge URL to the list of allowed URLs:
    *   `Tools` -> `Options` -> `Expert Advisors` -> `Allow WebRequest for listed URL`.

### 3. Synchronize to VPS
1.  In the Navigator window, right-click on your **MQL5 VPS** subscription.
2.  Select **Synchronize Experts, Indicators and Signals**.
3.  Check the "Journal" tab of the VPS to confirm the EA has started successfully on the remote server.

## 🔍 Monitoring
*   Monitor trades via the MT5 mobile app or the terminal on your local device.
*   Bridge logs on `WIN-DNGG6AODSKQ` will show incoming signals from the VPS.

---
**Broker**: FxPro
**Server**: FxPro-MT5 (or as specified in your account details)
**Account Type**: Standard
