# FxPro MT5 Standard Trading Guide

This guide describes how to set up the GenX FX Trading System V4 for trading with an FxPro MT5 Standard account using the MetaTrader VPS service.

## 1. MetaTrader VPS Setup

1.  Open your MetaTrader 5 terminal on your local machine (Asus Vivobook or Mini PC).
2.  Log in to your **FxPro-MT5 Standard** account.
    *   **Note**: Standard accounts typically use the **'m' suffix** for symbols (e.g., `EURUSDm`). Ensure you have these symbols enabled in your 'Market Watch'.
3.  Right-click on your account in the 'Navigator' window and select **'Register a Virtual Server'**.
4.  Follow the instructions to subscribe and choose the server with the lowest latency to FxPro.

## 2. EA Deployment

1.  In your local MT5, copy `GenX_EA_V4.mq5` to the `MQL5/Experts` folder.
2.  Open the EA in MetaEditor and **Compile** it.
4.  Back in MT5, drag the EA onto a chart (e.g., `EURUSDm`).
4.  Configure the following Input Parameters:
    *   `JULES_API_KEY_V4`: Your secure API Key.
    *   `GITHUB_TOKEN_PUSH`: Your GitHub Personal Access Token.
    *   `BridgeURL`: The URL of your local bridge (see section 3).
5.  Synchronize the terminal with the VPS (Tools -> Virtual Hosting -> Synchronize Experts, Indicators).

## 3. Local Bridge Configuration (Mini PC / Laptop)

Since the VPS runs in the cloud and your Bridge runs locally on `WIN-DNGG6AODSKQ` or your Vivobook, you must make the Bridge accessible to the VPS.

### Option A: Secure Tunnel (Recommended)
Use **Ngrok** or **Cloudflare Tunnel** to create a secure endpoint.

```bash
# Example using Ngrok
ngrok http 8000
```
Then, update the `BridgeURL` in the EA parameters on the VPS to the Ngrok URL (e.g., `https://random-id.ngrok-free.app`).

### Option B: Local Startup
On your Mini PC or Laptop, use the provided startup script:

```bash
# Start with FxPro configuration
./start_all.sh --env GenX_FX_V4/.env.fxpro
```

## 4. Monitoring

*   Check the 'Journal' tab on the MetaTrader VPS to ensure the EA is sending signals.
*   Monitor the Bridge console output on your local device to verify data ingestion.
*   Performance metrics will be synced to Firestore (if configured) and the performance repository.
