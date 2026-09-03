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

    def test_filters_transactions_by_type(self) -> None:
        """Render only transactions matching the selected type."""
        response = self.client.get("/", {"transaction_type": "SALE"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "GT-1012")
        self.assertNotContains(response, "GT-1011")
        self.assertContains(response, "Gefilterte Datensätze")

    def test_paginates_transactions(self) -> None:
        """Render the second page of transactions."""
        response = self.client.get("/", {"page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "GT-1002")
        self.assertNotContains(response, "GT-1012")
        self.assertContains(response, "Seite 2 von 2")

    def test_invalid_dates_do_not_break_the_view(self) -> None:
        """Ignore invalid date filters while preserving their form values."""
        response = self.client.get(
            "/", {"date_from": "not-a-date", "date_to": "2026-06-27"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="not-a-date"')
        self.assertContains(response, 'value="2026-06-27"')
