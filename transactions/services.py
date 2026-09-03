from pathlib import Path

from django.conf import settings

from .repositories import CsvTransactionRepository, MongoTransactionRepository


def get_transaction_repository():
    if settings.TRANSACTION_DATA_SOURCE == "mongo":
        return MongoTransactionRepository(
            settings.MONGODB_URI,
            settings.MONGODB_DATABASE,
            settings.MONGODB_COLLECTION,
        )
    return CsvTransactionRepository(Path(settings.BASE_DIR) / "data" / "transactions.csv")
