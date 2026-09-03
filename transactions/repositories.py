from datetime import date
from decimal import Decimal
from typing import Protocol

from .domain import Transaction


class TransactionRepository(Protocol):
    def list(self, *, transaction_type: str = "", date_from: date | None = None, date_to: date | None = None) -> list[Transaction]: ...

    def count(self) -> int: ...


class CsvTransactionRepository:
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def list(self, *, transaction_type="", date_from=None, date_to=None):
        import csv

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
                if transaction_type and transaction.transaction_type != transaction_type:
                    continue
                if date_from and transaction.transaction_date < date_from:
                    continue
                if date_to and transaction.transaction_date > date_to:
                    continue
                transactions.append(transaction)
        return sorted(transactions, key=lambda item: item.transaction_date, reverse=True)

    def count(self):
        return len(self.list())


class MongoTransactionRepository:
    def __init__(self, uri, database, collection):
        from pymongo import MongoClient

        self.client = MongoClient(uri, serverSelectionTimeoutMS=2000)
        self.collection = self.client[database][collection]

    def list(self, *, transaction_type="", date_from=None, date_to=None):
        query = {}
        if transaction_type:
            query["transaction_type"] = transaction_type
        if date_from or date_to:
            query["transaction_date"] = {}
            if date_from:
                query["transaction_date"]["$gte"] = date_from.isoformat()
            if date_to:
                query["transaction_date"]["$lte"] = date_to.isoformat()
        return [self._to_domain(document) for document in self.collection.find(query).sort("transaction_date", -1)]

    def count(self):
        return self.collection.count_documents({})

    @staticmethod
    def _to_domain(document):
        return Transaction(
            transaction_id=document["transaction_id"],
            transaction_date=date.fromisoformat(document["transaction_date"]),
            transaction_type=document["transaction_type"],
            quantity_grams=Decimal(str(document["quantity_grams"])),
            price_eur=Decimal(str(document["price_eur"])),
            counterparty=document["counterparty"],
        )
