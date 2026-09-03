"""Management command for importing CSV transactions into MongoDB."""

from argparse import ArgumentParser
import csv
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from pymongo import MongoClient, UpdateOne


class Command(BaseCommand):
    """Import transaction data from a CSV file into MongoDB."""

    help = "Importiert die Beispieldaten aus CSV in MongoDB."

    def add_arguments(self, parser: ArgumentParser) -> None:
        """Register command-line arguments."""
        parser.add_argument(
            "--file",
            type=Path,
            default=Path(settings.BASE_DIR) / "data" / "transactions.csv",
        )
        parser.add_argument(
            "--clear", action="store_true", help="Leert die Collection vor dem Import."
        )

    def handle(self, *args: object, **options: object) -> None:
        """Import CSV rows into the configured MongoDB collection."""
        file_path = options["file"]
        if not isinstance(file_path, Path):
            raise TypeError("The --file argument must be a Path")
        with file_path.open(newline="", encoding="utf-8") as csv_file:
            documents = list(csv.DictReader(csv_file))
        for document in documents:
            document["quantity_grams"] = float(document["quantity_grams"])
            document["price_eur"] = float(document["price_eur"])
        with MongoClient(settings.MONGODB_URI) as client:
            collection = client[settings.MONGODB_DATABASE][settings.MONGODB_COLLECTION]
            if bool(options["clear"]):
                collection.delete_many({})
            collection.create_index("transaction_id", unique=True)
            result = collection.bulk_write(
                [
                    UpdateOne(
                        {"transaction_id": document["transaction_id"]},
                        {"$set": document},
                        upsert=True,
                    )
                    for document in documents
                ]
            )
        self.stdout.write(
            self.style.SUCCESS(
                f"{len(documents)} Datensätze importiert ({result.upserted_count} neu)."
            )
        )
