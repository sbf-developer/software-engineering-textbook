"""Small, dependency-free domain model used in the textbook."""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from uuid import uuid4


class ValidationError(ValueError):
    """Raised when a request violates a domain invariant."""


@dataclass(frozen=True)
class LineItem:
    sku: str
    quantity: int
    unit_price_cents: int


def _positive_int(value: object, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValidationError(f"{field} must be a positive integer")
    return value


def total_cents(items: list[dict[str, object]] | list[LineItem]) -> int:
    """Return an exact integer-money total; floating point is not used."""
    if not items:
        raise ValidationError("an order needs at least one line item")
    total = 0
    for item in items:
        if isinstance(item, LineItem):
            quantity = item.quantity
            price = item.unit_price_cents
            sku = item.sku
        else:
            quantity = item.get("quantity")
            price = item.get("unit_price_cents")
            sku = item.get("sku")
        quantity = _positive_int(quantity, "quantity")
        price = _positive_int(price, "unit_price_cents")
        if not isinstance(sku, str) or not sku.strip() or len(sku) > 64:
            raise ValidationError("sku must be a non-empty string of at most 64 characters")
        total += quantity * price
    return total


def tax_cents(subtotal_cents: int, rate: str = "0.25") -> int:
    """Calculate a tax amount with decimal arithmetic and half-up rounding."""
    _positive_int(subtotal_cents, "subtotal_cents")
    value = (Decimal(subtotal_cents) * Decimal(rate)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    return int(value)


def create_order(customer_id: str, items: list[dict[str, object]]) -> dict[str, object]:
    if not isinstance(customer_id, str) or not customer_id.strip():
        raise ValidationError("customer_id is required")
    subtotal = total_cents(items)
    return {
        "id": str(uuid4()),
        "customer_id": customer_id,
        "items": items,
        "subtotal_cents": subtotal,
        "total_cents": subtotal + tax_cents(subtotal),
        "status": "accepted",
    }

