# A6-9V Trading System Blueprint - AI Agent Integration

This document outlines the architecture and data flow for the GenX FX Trading System V4, specifically configured for AI agent trading on device **WIN-DNGG6AODSKQ** using WSL2.

## 🏗️ System Architecture

The system consists of three primary layers:

1.  **Signal Generation Layer (MQL5 EA)**:
    *   **Component**: `GenX_EA_V4.mq5` running in MetaTrader 5.
    *   **Function**: Captures market ticks, account status, and indicator signals.
    *   **Communication**: Sends JSON payloads via `WebRequest` to the Bridge API Gateway.

2.  **API Gateway Layer (Python Bridge)**:
    *   **Component**: `GenX_FX_V4/bridge.py` (running in WSL2).
    *   **Function**: Acts as a secure intermediary. It validates authentication tokens and routes data between the EA and the AI Agent.
    *   **Endpoints**:
        *   `POST /`: Default endpoint for EA signal ingestion.
        *   `POST /ai-trade`: Dedicated endpoint for AI Agent trading logic and execution commands.

3.  **AI Agent Layer (Trading Intelligence)**:
    *   **Component**: AI Agent (Logic/Execution).
    *   *Function**: Processes market data from the Bridge, applies trading strategies, and sends execution signals back to the Bridge for routing to MT5 (via future order execution extensions).

## 🔑 Authentication & Security

The system uses multiple tiers of authentication:

*   **JULES_API_KEY_V4**: Primary bearer token for internal bridge communication.
*   **GITHUB_TOKEN_PUSH**: Required for performance tracking and repository synchronization.
*   **AI Agent API Keys (AQ.)**:
    *   (Refer to secure environment configuration or `.env` files for key values)
    *   Key 1: Primary Logic
    *   Key 2: Secondary/Backup
    *   Key 3: Monitoring/Audit

## 💻 Environment Configuration

*   **Device Name**: `WIN-DNGG6AODSKQ`
*   **Platform**: Windows 11 with WSL2 (Ubuntu/Debian)
*   **Orchestration**: `start_all.sh` provides unified initialization for both the Trading Bridge and infrastructure.

## 📡 Data Flow Mapping

1.  **Market Tick**: MT5 -> `GenX_EA_V4.mq5`
2.  **Signal Dispatch**: `GenX_EA_V4.mq5` -> `POST /` (Bridge)
3.  **AI Intelligence Request**: Bridge -> AI Agent (Logic Processing)
4.  **Trade Execution Command**: AI Agent -> `POST /ai-trade` (Bridge) -> MT5 (Execution)

---
**Last Updated**: 2026-05-06
