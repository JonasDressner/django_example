# Goldtransaktionen - Django & MongoDB

Django-Anwendung zur Verwaltung und Anzeige von Goldtransaktionen mit CSV- und MongoDB-Datenquellen.

## Schnellstart

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
pre-commit install
python manage.py runserver
```

Danach ist die Übersicht unter http://127.0.0.1:8000 erreichbar.

Das Projekt wurde mit Python 3.14 entwickelt und getestet.

## Testdaten aus CSV

Standardmäßig verwendet die Anwendung die reproduzierbaren Beispieldaten aus
`data/transactions.csv`. Dadurch kann die Anwendung lokal ausgeführt und getestet
werden, ohne dass eine MongoDB-Instanz erforderlich ist.

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
pre-commit run --all-files
```

## Architektur

- `transactions/domain.py`: Framework-unabhängiges Transaktionsmodell
- `transactions/repositories.py`: austauschbare CSV- und MongoDB-Adapter
- `transactions/services.py`: Auswahl der Datenquelle über Konfiguration
- `transactions/views.py`: dünne HTTP-Schicht mit Filterung und Pagination
- `data/transactions.csv`: reproduzierbare Demo-Daten
