"""Application services for selecting a transaction data source."""

from pathlib import Path

from django.conf import settings

from .repositories import CsvTransactionRepository, MongoTransactionRepository


def get_transaction_repository() -> (
    CsvTransactionRepository | MongoTransactionRepository
):
    """Return the repository configured for the current environment."""
    if settings.TRANSACTION_DATA_SOURCE == "mongo":
        return MongoTransactionRepository(
            settings.MONGODB_URI,
            settings.MONGODB_DATABASE,
            settings.MONGODB_COLLECTION,
        )
    return CsvTransactionRepository(
        Path(settings.BASE_DIR) / "data" / "transactions.csv"
    )
