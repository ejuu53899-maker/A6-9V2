import os
from fastapi import FastAPI, HTTPException, Request, Depends, Security
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ZOLO-Bridge")

app = FastAPI(title="ZOLO Bridge API")

# Security Configuration
API_KEY_NAME = "X-Bridge-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# CORS Configuration
ALLOWED_ORIGINS = [
    "https://genx-fx.com",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_api_key(api_key: str = Security(api_key_header)):
    expected_key = os.getenv("BRIDGE_API_KEY")
    if not expected_key:
        logger.warning("BRIDGE_API_KEY not set in environment!")
        # For development/safety, if not set, deny all
        raise HTTPException(status_code=500, detail="Bridge Security Not Configured")

    if api_key == expected_key:
        return api_key

    logger.warning(f"Unauthorized access attempt with key: {api_key}")
    raise HTTPException(status_code=403, detail="Invalid Bridge API Key")

# Signal models
class TradeSignal(BaseModel):
    symbol: str
    action: str  # BUY, SELL, CLOSE
    broker: Optional[str] = "EXNESS"
    lot_size: Optional[float] = 0.01
    stop_loss: Optional[float] = 0.0
    take_profit: Optional[float] = 0.0
    comment: Optional[str] = ""
    signal_id: Optional[str] = ""

# In-memory signal queue (simplified)
signal_queue: List[TradeSignal] = []

@app.get("/")
async def root():
    return {"status": "online", "message": "ZOLO Bridge is active and secured"}

@app.post("/api/signal", dependencies=[Depends(get_api_key)])
async def receive_signal(signal: TradeSignal):
    logger.info(f"Received signal: {signal.symbol} {signal.action}")
    signal_queue.append(signal)
    return {"status": "received", "signal_id": signal.signal_id}

@app.get("/api/get_signals", dependencies=[Depends(get_api_key)])
async def get_signals():
    global signal_queue
    signals = signal_queue.copy()
    signal_queue = []
    return signals

@app.post("/api/status", dependencies=[Depends(get_api_key)])
async def update_status(status_data: dict):
    logger.info(f"Status update received")
    return {"status": "ok"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
