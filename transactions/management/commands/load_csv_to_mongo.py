import csv
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from pymongo import MongoClient, UpdateOne


class Command(BaseCommand):
    help = "Importiert die Beispieldaten aus CSV in MongoDB."

    def add_arguments(self, parser):
        parser.add_argument("--file", type=Path, default=Path(settings.BASE_DIR) / "data" / "transactions.csv")
        parser.add_argument("--clear", action="store_true", help="Leert die Collection vor dem Import.")

    def handle(self, *args, **options):
        client = MongoClient(settings.MONGODB_URI)
        collection = client[settings.MONGODB_DATABASE][settings.MONGODB_COLLECTION]
        if options["clear"]:
            collection.delete_many({})
        with options["file"].open(newline="", encoding="utf-8") as csv_file:
            documents = list(csv.DictReader(csv_file))
        for document in documents:
            document["quantity_grams"] = float(document["quantity_grams"])
            document["price_eur"] = float(document["price_eur"])
        collection.create_index("transaction_id", unique=True)
        result = collection.bulk_write([
            UpdateOne(
                {"transaction_id": document["transaction_id"]},
                {"$set": document},
                upsert=True,
            )
            for document in documents
        ])
        self.stdout.write(self.style.SUCCESS(f"{len(documents)} Datensätze importiert ({result.upserted_count} neu)."))
