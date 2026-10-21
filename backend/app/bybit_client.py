import asyncio
import json
import logging
import websockets
from typing import Callable, Optional
from .models import OrderBookSnapshot, OrderBookDelta, PriceLevel, Trade
from .orderbook import OrderBookEngine

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class BybitWebsocketClient:
    def __init__(self, url: str, symbol: str, on_orderbook_update: Callable, on_trade_update: Callable):
        self.url = url
        self.symbol = symbol
        self.on_orderbook_update = on_orderbook_update
        self.on_trade_update = on_trade_update
        self.orderbook_engine = OrderBookEngine(symbol)
        self.running = False
        self.ws = None

    async def connect(self):
        self.running = True
        while self.running:
            try:
                async with websockets.connect(self.url) as ws:
                    self.ws = ws
                    logger.info(f"Connected to Bybit public websocket: {self.url}")

                    # Subscribe to orderbook (depth 50) and public trades
                    subscribe_msg = {
                        "op": "subscribe",
                        "args": [
                            f"orderbook.50.{self.symbol}",
                            f"publicTrade.{self.symbol}"
                        ]
                    }
                    await ws.send(json.dumps(subscribe_msg))

                    await self._listen(ws)
            except websockets.exceptions.ConnectionClosed:
                logger.warning("Websocket connection closed. Reconnecting in 2 seconds...")
                await asyncio.sleep(2)
            except Exception as e:
                logger.error(f"Websocket error: {e}. Reconnecting in 2 seconds...")
                await asyncio.sleep(2)

    async def stop(self):
        self.running = False
        if self.ws:
            await self.ws.close()

    async def _listen(self, ws):
        async for msg in ws:
            data = json.loads(msg)

            if "topic" not in data:
                continue

            topic = data["topic"]
            if topic.startswith("orderbook"):
                self._handle_orderbook(data)
            elif topic.startswith("publicTrade"):
                self._handle_trade(data)

    def _handle_orderbook(self, data: dict):
        topic_type = data.get("type")
        payload = data.get("data", {})

        bids = [PriceLevel(price=float(p[0]), size=float(p[1])) for p in payload.get("b", [])]
        asks = [PriceLevel(price=float(p[0]), size=float(p[1])) for p in payload.get("a", [])]

        u = payload.get("u", 0)
        seq = payload.get("seq", 0)

        if topic_type == "snapshot":
            snapshot = OrderBookSnapshot(
                symbol=self.symbol,
                bids=bids,
                asks=asks,
                u=u,
                seq=seq
            )
            self.orderbook_engine.apply_snapshot(snapshot)
            # Notify callback
            asyncio.create_task(self.on_orderbook_update(self.orderbook_engine.get_top_levels(20)))

        elif topic_type == "delta":
            delta = OrderBookDelta(
                symbol=self.symbol,
                bids=bids,
                asks=asks,
                u=u,
                seq=seq
            )
            success = self.orderbook_engine.apply_delta(delta)
            if not success:
                logger.warning("Delta applied before snapshot or out of sync.")
            else:
                # Notify callback
                asyncio.create_task(self.on_orderbook_update(self.orderbook_engine.get_top_levels(20)))

    def _handle_trade(self, data: dict):
        payloads = data.get("data", [])
        for p in payloads:
            trade = Trade(
                symbol=self.symbol,
                trade_id=p.get("i", ""),
                price=float(p.get("p", 0)),
                size=float(p.get("v", 0)),
                side=p.get("S", ""),
                timestamp=int(p.get("T", 0))
            )
            # Notify callback
            asyncio.create_task(self.on_trade_update(trade.dict()))
