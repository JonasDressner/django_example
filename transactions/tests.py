"""Tests for the transaction domain, repositories, and views."""

from datetime import date
from decimal import Decimal
from pathlib import Path

from django.test import TestCase

from .domain import Transaction
from .repositories import CsvTransactionRepository


class TransactionDomainTests(TestCase):
    """Test domain calculations."""

    def test_total_is_quantity_times_price(self) -> None:
        """Calculate the total from quantity and unit price."""
        transaction = Transaction(
            "GT-1", date(2026, 1, 1), "PURCHASE", Decimal("2.5"), Decimal("80"), "Test"
        )
        self.assertEqual(transaction.total_eur, Decimal("200.0"))


class CsvTransactionRepositoryTests(TestCase):
    """Test CSV repository behavior."""

    def setUp(self) -> None:
        """Create a repository backed by the fixture CSV."""
        self.repository = CsvTransactionRepository(
            Path(__file__).resolve().parent.parent / "data" / "transactions.csv"
        )

    def test_lists_newest_first(self) -> None:
        """Return transactions ordered from newest to oldest."""
        transactions = self.repository.list()
        self.assertEqual(len(transactions), 12)
        self.assertEqual(transactions[0].transaction_id, "GT-1012")

    def test_filters_by_type_and_date(self) -> None:
        """Filter transactions by type and start date."""
        transactions = self.repository.list(
            transaction_type="SALE", date_from=date(2026, 4, 1)
        )
        self.assertEqual(
            [item.transaction_id for item in transactions],
            ["GT-1012", "GT-1010", "GT-1008"],
        )


class TransactionViewTests(TestCase):
    """Test the transaction list view."""

    def test_homepage_renders_transactions(self) -> None:
        """Render the homepage with transaction data."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Transaktionsbuch")
