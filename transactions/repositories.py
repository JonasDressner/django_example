"""Repository implementations for CSV and MongoDB transactions."""

import csv

from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import TypedDict
from pymongo import MongoClient

from .domain import Transaction


class CsvTransactionRepository:
    """Read transactions from a CSV file."""

    def __init__(self, csv_path: Path) -> None:
        """Initialize the repository with a CSV file path."""
        self.csv_path = csv_path

    def list(
        self,
        *,
        transaction_type: str = "",
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> list[Transaction]:
        """Return CSV transactions matching the optional filters."""
        transactions = []
        with self.csv_path.open(newline="", encoding="utf-8") as csv_file:
            for row in csv.DictReader(csv_file):
                transaction = Transaction(
                    transaction_id=row["transaction_id"],
                    transaction_date=date.fromisoformat(row["transaction_date"]),
                    transaction_type=row["transaction_type"],
                    quantity_grams=Decimal(row["quantity_grams"]),
                    price_eur=Decimal(row["price_eur"]),
                    counterparty=row["counterparty"],
                )
                if (
                    transaction_type
                    and transaction.transaction_type != transaction_type
                ):
                    continue
                if date_from and transaction.transaction_date < date_from:
                    continue
                if date_to and transaction.transaction_date > date_to:
                    continue
                transactions.append(transaction)
        return sorted(
            transactions, key=lambda item: item.transaction_date, reverse=True
        )


class TransactionDocument(TypedDict):
    """Define the fields stored for a transaction in MongoDB."""

    transaction_id: str
    transaction_date: str
    transaction_type: str
    quantity_grams: float
    price_eur: float
    counterparty: str


class MongoTransactionRepository:
    """Read transactions from a MongoDB collection."""

    def __init__(self, uri: str, database: str, collection: str) -> None:
        """Initialize the repository with MongoDB connection settings."""
        self.client = MongoClient(uri, serverSelectionTimeoutMS=2000)
        self.collection = self.client[database][collection]

    def list(
        self,
        *,
        transaction_type: str = "",
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> list[Transaction]:
        """Return MongoDB transactions matching the optional filters."""
        query = {}
        if transaction_type:
            query["transaction_type"] = transaction_type
        if date_from or date_to:
            query["transaction_date"] = {}
            if date_from:
                query["transaction_date"]["$gte"] = date_from.isoformat()
            if date_to:
                query["transaction_date"]["$lte"] = date_to.isoformat()
        return [
            self._to_domain(document)
            for document in self.collection.find(query).sort("transaction_date", -1)
        ]

    @staticmethod
    def _to_domain(document: TransactionDocument) -> Transaction:
        """Convert a MongoDB document into a domain transaction."""
        return Transaction(
            transaction_id=document["transaction_id"],
            transaction_date=date.fromisoformat(document["transaction_date"]),
            transaction_type=document["transaction_type"],
            quantity_grams=Decimal(str(document["quantity_grams"])),
            price_eur=Decimal(str(document["price_eur"])),
            counterparty=document["counterparty"],
        )
