# Aurum Ledger

Ein vorzeigbares Django-Beispielprojekt zur Darstellung von Goldtransaktionen. Die Anwendung startet standardmäßig mit lokalen CSV-Testdaten und kann über dieselbe Repository-Schnittstelle auf MongoDB umgeschaltet werden.

## Schnellstart

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py runserver
```

Danach ist die Übersicht unter http://127.0.0.1:8000 erreichbar.

## MongoDB verwenden

MongoDB lokal starten:

```powershell
docker compose up -d mongodb
python manage.py load_csv_to_mongo --clear
```

In `.env` `TRANSACTION_DATA_SOURCE=mongo` setzen und den Server neu starten. Der Import ist wiederholbar, weil `transaction_id` als eindeutiger Schlüssel verwendet wird.

## Qualitätssicherung

```powershell
python manage.py check
pytest
```

## Architektur

- `transactions/domain.py`: Framework-unabhängiges Transaktionsmodell
- `transactions/repositories.py`: austauschbare CSV- und MongoDB-Adapter
- `transactions/services.py`: Auswahl der Datenquelle über Konfiguration
- `transactions/views.py`: dünne HTTP-Schicht mit Filterung und Pagination
- `data/transactions.csv`: reproduzierbare Demo-Daten
