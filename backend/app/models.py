from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class PriceLevel(BaseModel):
    price: float
    size: float

class OrderBookSnapshot(BaseModel):
    symbol: str
    bids: List[PriceLevel]
    asks: List[PriceLevel]
    u: int = Field(..., description="Update ID")
    seq: int = Field(..., description="Cross sequence number")

class OrderBookDelta(BaseModel):
    symbol: str
    bids: List[PriceLevel]
    asks: List[PriceLevel]
    u: int
    seq: int

class Trade(BaseModel):
    symbol: str
    trade_id: str
    price: float
    size: float
    side: str  # "Buy" or "Sell" (aggressor side)
    timestamp: int  # ms since epoch
