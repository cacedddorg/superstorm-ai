import asyncio
import json
import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import List

from app.bybit_client import BybitWebsocketClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BYBIT_WSS_URL = os.getenv("BYBIT_WSS_URL", "wss://stream.bybit.com/v5/public/linear")
SYMBOL = "BTCUSDT"

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")

manager = ConnectionManager()
bybit_client: BybitWebsocketClient = None

async def broadcast_orderbook(ob_data: dict):
    msg = {"type": "orderbook", "data": ob_data}
    await manager.broadcast(json.dumps(msg))

async def broadcast_trade(trade_data: dict):
    msg = {"type": "trade", "data": trade_data}
    await manager.broadcast(json.dumps(msg))

@asynccontextmanager
async def lifespan(app: FastAPI):
    global bybit_client
    logger.info("Starting Bybit WebSocket client...")
    bybit_client = BybitWebsocketClient(
        url=BYBIT_WSS_URL,
        symbol=SYMBOL,
        on_orderbook_update=broadcast_orderbook,
        on_trade_update=broadcast_trade
    )
    task = asyncio.create_task(bybit_client.connect())
    yield
    logger.info("Stopping Bybit WebSocket client...")
    await bybit_client.stop()
    task.cancel()

app = FastAPI(title="Superstorm AI Backend", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.websocket("/ws/market")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # We keep the connection open and wait for client disconnect
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket Error: {e}")
        manager.disconnect(websocket)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
