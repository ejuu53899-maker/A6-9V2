import os
import time
import asyncio
import logging
from dotenv import load_dotenv
import threading
import uvicorn
import requests
import sys

# Optional dependencies based on OS and availability
try:
    from pybit.unified_trading import HTTP as BybitHTTP
except ImportError:
    BybitHTTP = None

try:
    if sys.platform == "win32":
        import MetaTrader5 as mt5
    else:
        mt5 = None
except ImportError:
    mt5 = None

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("GenX-Trader")

# Load environment variables
load_dotenv()

def start_api_bridge():
    """Start the FastAPI bridge in a separate thread."""
    from api.main import app
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting API Bridge on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="error")

def execute_bybit_trade(signal: dict):
    """Execute trade on Bybit using the SDK."""
    if not BybitHTTP:
        logger.error("Bybit SDK (pybit) not installed. Skipping Bybit execution.")
        return False

    api_key = os.getenv("BYBIT_API_KEY")
    api_secret = os.getenv("BYBIT_SECRET_KEY")

    if not api_key or not api_secret:
        logger.warning("Bybit API credentials missing. Skipping Bybit execution.")
        return False

    symbol = signal.get("symbol")
    action = signal.get("action")
    side = "Buy" if action == "BUY" else "Sell"
    qty = float(signal.get("lot_size", 0.01))

    try:
        session = BybitHTTP(testnet=False, api_key=api_key, api_secret=api_secret)
        category = "linear" if "USDT" in symbol else "spot"

        response = session.place_order(
            category=category, symbol=symbol, side=side,
            orderType="Market", qty=str(qty), timeInForce="GTC"
        )

        if response.get("retCode") == 0:
            logger.info(f"BYBIT SUCCESS: {symbol} {side}")
            return True
        else:
            logger.error(f"BYBIT FAILED: {response.get('retMsg')}")
            return False
    except Exception as e:
        logger.error(f"Bybit API Exception: {e}")
        return False

def execute_mt5_trade(signal: dict):
    """Execute trade on MT5 (Windows Only)."""
    if not mt5:
        logger.error("MetaTrader5 library not available or not on Windows. Skipping MT5 execution.")
        return False

    if not mt5.initialize():
        logger.error("MT5 initialize() failed")
        return False

    symbol = signal.get("symbol")
    action = signal.get("action")
    lot = float(signal.get("lot_size", 0.1))

    # Login if credentials provided
    login = int(os.getenv("MT5_ACCOUNT_ID", 0))
    password = os.getenv("MT5_PASSWORD", "")
    server = os.getenv("MT5_SERVER", "")

    if login > 0:
        if not mt5.login(login, password=password, server=server):
            logger.error(f"MT5 Login failed for {login}")
            return False

    # Prep request
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        logger.error(f"Symbol {symbol} not found in MT5")
        return False

    if not symbol_info.visible:
        if not mt5.symbol_select(symbol, True):
            logger.error(f"Failed to select symbol {symbol}")
            return False

    price = mt5.symbol_info_tick(symbol).ask if action == "BUY" else mt5.symbol_info_tick(symbol).bid
    order_type = mt5.ORDER_TYPE_BUY if action == "BUY" else mt5.ORDER_TYPE_SELL

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "magic": 26012025,
        "comment": signal.get("comment", "GenX Autonomous"),
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        logger.error(f"MT5 Trade FAILED: {result.comment} (Code: {result.retcode})")
        return False

    logger.info(f"MT5 SUCCESS: {symbol} {action} | Ticket: {result.order}")
    return True

def execute_trade(signal: dict):
    """Orchestrate trade execution across different brokers."""
    symbol = signal.get("symbol")
    action = signal.get("action")

    is_crypto = any(crypto in symbol.upper() for crypto in ["BTC", "ETH", "USDT", "SOL", "XRP"])

    success = False
    if is_crypto:
        success = execute_bybit_trade(signal)
    else:
        if sys.platform == "win32":
            success = execute_mt5_trade(signal)
        else:
            logger.info(f"HEADLESS SIMULATION: {action} {symbol} (MT5 requires Windows)")
            success = True # Assume success for simulation purposes

    if success:
        # Notify back to bridge
        port = os.environ.get("PORT", 8080)
        bridge_key = os.getenv("BRIDGE_API_KEY")
        headers = {"X-Bridge-Key": bridge_key}
        try:
            requests.post(f"http://localhost:{port}/api/status", json={"status": "executed", "symbol": symbol}, headers=headers)
        except: pass

async def monitor_signals():
    port = os.environ.get("PORT", 8080)
    bridge_url = f"http://localhost:{port}/api/get_signals"
    bridge_key = os.getenv("BRIDGE_API_KEY")
    headers = {"X-Bridge-Key": bridge_key}

    logger.info(f"Monitoring {bridge_url}...")
    while True:
        try:
            response = requests.get(bridge_url, headers=headers)
            if response.status_code == 200:
                for signal in response.json():
                    execute_trade(signal)
        except Exception as e:
            logger.error(f"Loop Error: {e}")
        await asyncio.sleep(2)

async def main_loop():
    if not os.getenv("BRIDGE_API_KEY"):
        logger.critical("No BRIDGE_API_KEY!")
        return

    threading.Thread(target=start_api_bridge, daemon=True).start()
    await asyncio.sleep(2)
    logger.info("Autonomous Trading System active.")
    await monitor_signals()

if __name__ == "__main__":
    try: asyncio.run(main_loop())
    except KeyboardInterrupt: logger.info("Shutting down.")
