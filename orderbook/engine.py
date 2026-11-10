"""Crypto L2 Limit Order Book (LOB) Price-Time Priority Matching Engine."""

import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class Order(BaseModel):
    order_id: str
    symbol: str  # e.g., BTC-USDT, ETH-INR
    side: str    # BUY (Bid) or SELL (Ask)
    price: float
    quantity: float
    remaining_quantity: float
    timestamp: float = Field(default_factory=time.time)


class TradeExecution(BaseModel):
    trade_id: str
    symbol: str
    maker_order_id: str
    taker_order_id: str
    executed_price: float
    executed_quantity: float
    timestamp: float = Field(default_factory=time.time)


class MatchingEngine:
    """In-memory Price-Time Priority FIFO Matching Engine for Spot Crypto Trading."""

    def __init__(self, symbol: str = "BTC-USDT"):
        self.symbol = symbol
        self.bids: List[Order] = []  # sorted descending by price, then ascending by time
        self.asks: List[Order] = []  # sorted ascending by price, then ascending by time
        self.trade_history: List[TradeExecution] = []

    def place_order(self, side: str, price: float, quantity: float, order_id: Optional[str] = None) -> Dict[str, Any]:
        side = side.upper()
        if side not in ("BUY", "SELL"):
            raise ValueError("Side must be BUY or SELL.")
        if price <= 0 or quantity <= 0:
            raise ValueError("Price and quantity must be positive numbers.")

        order = Order(
            order_id=order_id or f"ORD-{uuid.uuid4().hex[:8].upper()}",
            symbol=self.symbol,
            side=side,
            price=round(price, 2),
            quantity=round(quantity, 4),
            remaining_quantity=round(quantity, 4),
            timestamp=time.time()
        )

        fills: List[TradeExecution] = []

        if side == "BUY":
            # Match against existing Ask orders where ask.price <= buy.price
            while self.asks and order.remaining_quantity > 0:
                best_ask = self.asks[0]
                if best_ask.price > order.price:
                    break  # no more matchable asks

                match_qty = min(order.remaining_quantity, best_ask.remaining_quantity)
                order.remaining_quantity -= match_qty
                best_ask.remaining_quantity -= match_qty

                trade = TradeExecution(
                    trade_id=f"TRD-{uuid.uuid4().hex[:8].upper()}",
                    symbol=self.symbol,
                    maker_order_id=best_ask.order_id,
                    taker_order_id=order.order_id,
                    executed_price=best_ask.price,
                    executed_quantity=match_qty
                )
                fills.append(trade)
                self.trade_history.append(trade)

                if best_ask.remaining_quantity <= 0:
                    self.asks.pop(0)

            # If leftover, add to bid book (sorted descending by price, ascending time)
            if order.remaining_quantity > 0:
                self.bids.append(order)
                self.bids.sort(key=lambda x: (-x.price, x.timestamp))

        else:  # SELL order
            # Match against existing Bid orders where bid.price >= sell.price
            while self.bids and order.remaining_quantity > 0:
                best_bid = self.bids[0]
                if best_bid.price < order.price:
                    break  # no more matchable bids

                match_qty = min(order.remaining_quantity, best_bid.remaining_quantity)
                order.remaining_quantity -= match_qty
                best_bid.remaining_quantity -= match_qty

                trade = TradeExecution(
                    trade_id=f"TRD-{uuid.uuid4().hex[:8].upper()}",
                    symbol=self.symbol,
                    maker_order_id=best_bid.order_id,
                    taker_order_id=order.order_id,
                    executed_price=best_bid.price,
                    executed_quantity=match_qty
                )
                fills.append(trade)
                self.trade_history.append(trade)

                if best_bid.remaining_quantity <= 0:
                    self.bids.pop(0)

            # If leftover, add to ask book (sorted ascending by price, ascending time)
            if order.remaining_quantity > 0:
                self.asks.append(order)
                self.asks.sort(key=lambda x: (x.price, x.timestamp))

        return {
            "order_id": order.order_id,
            "side": order.side,
            "status": "FILLED" if order.remaining_quantity == 0 else ("PARTIAL" if len(fills) > 0 else "OPEN"),
            "filled_quantity": round(order.quantity - order.remaining_quantity, 4),
            "remaining_quantity": round(order.remaining_quantity, 4),
            "trades": [f.model_dump() for f in fills]
        }

    def get_order_book_depth(self) -> Dict[str, Any]:
        """Returns top Level 2 depth snapshot."""
        best_bid = self.bids[0].price if self.bids else None
        best_ask = self.asks[0].price if self.asks else None
        spread = round(best_ask - best_bid, 2) if (best_bid and best_ask) else None

        return {
            "symbol": self.symbol,
            "best_bid": best_bid,
            "best_ask": best_ask,
            "spread": spread,
            "bid_depth_count": len(self.bids),
            "ask_depth_count": len(self.asks)
        }
