"""Domain model for gold transactions."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class Transaction:
    """Represent one gold transaction."""

    transaction_id: str
    transaction_date: date
    transaction_type: str
    quantity_grams: Decimal
    price_eur: Decimal
    counterparty: str

    @property
    def total_eur(self) -> Decimal:
        """Return the transaction value in euros."""
        return self.quantity_grams * self.price_eur
