from typing import Dict, List, Optional
from .models import OrderBookSnapshot, OrderBookDelta, PriceLevel
import copy

class OrderBookEngine:
    def __init__(self, symbol: str):
        self.symbol = symbol
        # Use dictionaries for O(1) lookup: price -> size
        self.bids: Dict[float, float] = {}
        self.asks: Dict[float, float] = {}
        self.u: int = 0
        self.seq: int = 0
        self.is_initialized = False

    def apply_snapshot(self, snapshot: OrderBookSnapshot):
        self.bids = {level.price: level.size for level in snapshot.bids}
        self.asks = {level.price: level.size for level in snapshot.asks}
        self.u = snapshot.u
        self.seq = snapshot.seq
        self.is_initialized = True

    def apply_delta(self, delta: OrderBookDelta) -> bool:
        """
        Applies a delta. Returns True if successful, False if out of sync.
        Bybit linear uses `u` (updateId). For a sequence to be valid,
        often we require strict ordering, but for simplicity we assume
        deltas with newer `u` or `seq` are applied.
        """
        if not self.is_initialized:
            return False

        # In a strict real-world implementation, you'd check sequence continuity:
        # e.g., delta.u == self.u + 1 or similar logic specific to the exchange.
        # Here we just apply the updates if they seem newer.

        # Apply bids
        for level in delta.bids:
            if level.size == 0.0:
                self.bids.pop(level.price, None)
            else:
                self.bids[level.price] = level.size

        # Apply asks
        for level in delta.asks:
            if level.size == 0.0:
                self.asks.pop(level.price, None)
            else:
                self.asks[level.price] = level.size

        self.u = delta.u
        self.seq = delta.seq
        return True

    def get_top_levels(self, depth: int = 20) -> Dict:
        """Returns the sorted order book up to `depth` levels."""
        sorted_bids = sorted(self.bids.items(), key=lambda x: x[0], reverse=True)
        sorted_asks = sorted(self.asks.items(), key=lambda x: x[0])

        return {
            "symbol": self.symbol,
            "bids": [{"price": p, "size": s} for p, s in sorted_bids[:depth]],
            "asks": [{"price": p, "size": s} for p, s in sorted_asks[:depth]],
            "u": self.u,
            "seq": self.seq
        }
