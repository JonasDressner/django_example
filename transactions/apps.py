"""Django application configuration for transactions."""

from django.apps import AppConfig


class TransactionsConfig(AppConfig):
    """Configure the transactions Django application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "transactions"
