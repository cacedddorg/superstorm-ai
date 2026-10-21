import pytest
from app.models import OrderBookSnapshot, OrderBookDelta, PriceLevel
from app.orderbook import OrderBookEngine

def test_orderbook_engine_snapshot():
    engine = OrderBookEngine("BTCUSDT")
    snapshot = OrderBookSnapshot(
        symbol="BTCUSDT",
        bids=[PriceLevel(price=100.0, size=1.0), PriceLevel(price=99.0, size=2.0)],
        asks=[PriceLevel(price=101.0, size=1.0), PriceLevel(price=102.0, size=2.0)],
        u=10,
        seq=100
    )

    engine.apply_snapshot(snapshot)

    assert engine.is_initialized is True
    assert engine.bids[100.0] == 1.0
    assert engine.asks[101.0] == 1.0
    assert engine.u == 10
    assert engine.seq == 100

def test_orderbook_engine_delta():
    engine = OrderBookEngine("BTCUSDT")
    # Must initialize with snapshot first
    snapshot = OrderBookSnapshot(
        symbol="BTCUSDT",
        bids=[PriceLevel(price=100.0, size=1.0)],
        asks=[PriceLevel(price=101.0, size=1.0)],
        u=10,
        seq=100
    )
    engine.apply_snapshot(snapshot)

    # Apply delta to add a bid, update an ask, and remove a bid
    delta = OrderBookDelta(
        symbol="BTCUSDT",
        bids=[PriceLevel(price=100.0, size=0.0), PriceLevel(price=99.5, size=5.0)],
        asks=[PriceLevel(price=101.0, size=2.5)],
        u=11,
        seq=101
    )
    success = engine.apply_delta(delta)

    assert success is True
    assert 100.0 not in engine.bids  # Removed
    assert engine.bids[99.5] == 5.0  # Added
    assert engine.asks[101.0] == 2.5 # Updated size
    assert engine.u == 11

def test_orderbook_engine_delta_before_snapshot():
    engine = OrderBookEngine("BTCUSDT")
    delta = OrderBookDelta(
        symbol="BTCUSDT",
        bids=[PriceLevel(price=100.0, size=1.0)],
        asks=[],
        u=1,
        seq=1
    )
    success = engine.apply_delta(delta)
    assert success is False
    assert engine.is_initialized is False

def test_orderbook_get_top_levels():
    engine = OrderBookEngine("BTCUSDT")
    snapshot = OrderBookSnapshot(
        symbol="BTCUSDT",
        bids=[PriceLevel(price=99.0, size=2.0), PriceLevel(price=100.0, size=1.0)],
        asks=[PriceLevel(price=102.0, size=2.0), PriceLevel(price=101.0, size=1.0)],
        u=10,
        seq=100
    )
    engine.apply_snapshot(snapshot)

    top_levels = engine.get_top_levels(10)
    # Bids should be sorted descending
    assert top_levels["bids"][0]["price"] == 100.0
    assert top_levels["bids"][1]["price"] == 99.0
    # Asks should be sorted ascending
    assert top_levels["asks"][0]["price"] == 101.0
    assert top_levels["asks"][1]["price"] == 102.0
