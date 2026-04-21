"""
Order placement logic for Binance Futures Testnet.

Builds the correct parameter payload for each order type,
delegates to the API client, and returns a structured result.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from bot.client import BinanceClient

logger = logging.getLogger(__name__)


@dataclass
class OrderResult:
    """Normalised view of a Binance order response."""

    order_id: int
    symbol: str
    side: str
    order_type: str
    status: str
    orig_qty: str
    executed_qty: str
    avg_price: str
    price: str
    raw: dict[str, Any]

    def display(self) -> None:
        """Pretty-print the order result to stdout."""
        sep = "─" * 52
        print(f"\n{'✅ Order placed successfully':^52}")
        print(sep)
        print(f"  Order ID    : {self.order_id}")
        print(f"  Symbol      : {self.symbol}")
        print(f"  Side        : {self.side}")
        print(f"  Type        : {self.order_type}")
        print(f"  Status      : {self.status}")
        print(f"  Quantity    : {self.orig_qty}")
        print(f"  Executed    : {self.executed_qty}")
        print(f"  Avg Price   : {self.avg_price or 'N/A'}")
        print(f"  Limit Price : {self.price or 'N/A'}")
        print(sep)


def _parse_response(data: dict[str, Any]) -> OrderResult:
    return OrderResult(
        order_id=data.get("orderId", 0),
        symbol=data.get("symbol", ""),
        side=data.get("side", ""),
        order_type=data.get("type", ""),
        status=data.get("status", ""),
        orig_qty=data.get("origQty", "0"),
        executed_qty=data.get("executedQty", "0"),
        avg_price=data.get("avgPrice", ""),
        price=data.get("price", ""),
        raw=data,
    )


class OrderManager:
    """
    High-level order management layer.

    Args:
        client: Authenticated BinanceClient instance.
    """

    def __init__(self, client: BinanceClient) -> None:
        self._client = client

    def place_market_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
    ) -> OrderResult:
        """Place a MARKET order."""
        params = {
            "symbol": symbol,
            "side": side,
            "type": "MARKET",
            "quantity": quantity,
        }
        logger.info(
            "Market order | symbol=%s side=%s qty=%s", symbol, side, quantity
        )
        print(f"\n📤 Sending MARKET order → {symbol} | {side} | qty={quantity}")
        data = self._client.place_order(params)
        return _parse_response(data)

    def place_limit_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        price: float,
        time_in_force: str = "GTC",
    ) -> OrderResult:
        """Place a LIMIT order."""
        params = {
            "symbol": symbol,
            "side": side,
            "type": "LIMIT",
            "quantity": quantity,
            "price": price,
            "timeInForce": time_in_force,
        }
        logger.info(
            "Limit order | symbol=%s side=%s qty=%s price=%s",
            symbol,
            side,
            quantity,
            price,
        )
        print(
            f"\n📤 Sending LIMIT order → {symbol} | {side} | qty={quantity} | price={price}"
        )
        data = self._client.place_order(params)
        return _parse_response(data)

    def place_stop_market_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        stop_price: float,
    ) -> OrderResult:
        """Place a STOP_MARKET order (bonus order type)."""
        params = {
            "symbol": symbol,
            "side": side,
            "type": "STOP_MARKET",
            "quantity": quantity,
            "stopPrice": stop_price,
        }
        logger.info(
            "Stop-Market order | symbol=%s side=%s qty=%s stopPrice=%s",
            symbol,
            side,
            quantity,
            stop_price,
        )
        print(
            f"\n📤 Sending STOP_MARKET order → {symbol} | {side} "
            f"| qty={quantity} | stopPrice={stop_price}"
        )
        data = self._client.place_order(params)
        return _parse_response(data)

    def place_stop_limit_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        price: float,
        stop_price: float,
        time_in_force: str = "GTC",
    ) -> OrderResult:
        """Place a STOP (stop-limit) order (bonus order type)."""
        params = {
            "symbol": symbol,
            "side": side,
            "type": "STOP",
            "quantity": quantity,
            "price": price,
            "stopPrice": stop_price,
            "timeInForce": time_in_force,
        }
        logger.info(
            "Stop-Limit order | symbol=%s side=%s qty=%s price=%s stopPrice=%s",
            symbol,
            side,
            quantity,
            price,
            stop_price,
        )
        print(
            f"\n📤 Sending STOP_LIMIT order → {symbol} | {side} "
            f"| qty={quantity} | price={price} | stopPrice={stop_price}"
        )
        data = self._client.place_order(params)
        return _parse_response(data)
