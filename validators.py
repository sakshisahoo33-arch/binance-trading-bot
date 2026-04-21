"""
Input validation for CLI arguments.
"""

from __future__ import annotations

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_MARKET", "STOP_LIMIT"}


class ValidationError(ValueError):
    """Raised when user-supplied input fails validation."""


def validate_symbol(symbol: str) -> str:
    """Validate and normalise a trading symbol."""
    symbol = symbol.strip().upper()
    if not symbol.isalnum():
        raise ValidationError(
            f"Invalid symbol '{symbol}'. Must be alphanumeric (e.g. BTCUSDT)."
        )
    if len(symbol) < 5:
        raise ValidationError(
            f"Symbol '{symbol}' looks too short. Expected something like BTCUSDT."
        )
    return symbol


def validate_side(side: str) -> str:
    """Validate order side."""
    side = side.strip().upper()
    if side not in VALID_SIDES:
        raise ValidationError(
            f"Invalid side '{side}'. Must be one of: {', '.join(sorted(VALID_SIDES))}."
        )
    return side


def validate_order_type(order_type: str) -> str:
    """Validate order type."""
    order_type = order_type.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValidationError(
            f"Invalid order type '{order_type}'. "
            f"Must be one of: {', '.join(sorted(VALID_ORDER_TYPES))}."
        )
    return order_type


def validate_quantity(quantity: str | float) -> float:
    """Validate order quantity."""
    try:
        qty = float(quantity)
    except (TypeError, ValueError):
        raise ValidationError(f"Quantity '{quantity}' is not a valid number.")
    if qty <= 0:
        raise ValidationError(f"Quantity must be greater than 0. Got: {qty}.")
    return qty


def validate_price(price: str | float | None, order_type: str) -> float | None:
    """Validate price for the given order type."""
    if order_type in ("LIMIT", "STOP_LIMIT"):
        if price is None:
            raise ValidationError(
                f"Price is required for {order_type} orders."
            )
        try:
            p = float(price)
        except (TypeError, ValueError):
            raise ValidationError(f"Price '{price}' is not a valid number.")
        if p <= 0:
            raise ValidationError(f"Price must be greater than 0. Got: {p}.")
        return p

    if price is not None:
        # Allow but warn; price is ignored for MARKET/STOP_MARKET
        pass

    return None


def validate_stop_price(stop_price: str | float | None, order_type: str) -> float | None:
    """Validate stop price for stop orders."""
    if order_type in ("STOP_MARKET", "STOP_LIMIT"):
        if stop_price is None:
            raise ValidationError(
                f"Stop price (--stop-price) is required for {order_type} orders."
            )
        try:
            sp = float(stop_price)
        except (TypeError, ValueError):
            raise ValidationError(f"Stop price '{stop_price}' is not a valid number.")
        if sp <= 0:
            raise ValidationError(f"Stop price must be greater than 0. Got: {sp}.")
        return sp
    return None
