"""HTTP views for displaying transactions."""

from datetime import date

from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .services import get_transaction_repository

PAGE_SIZE = 10


def transaction_list(request: HttpRequest) -> HttpResponse:
    """Render the filtered and paginated transaction list."""
    date_from_value = request.GET.get("date_from", "")
    date_to_value = request.GET.get("date_to", "")
    date_from = _parse_date(date_from_value)
    date_to = _parse_date(date_to_value)
    transaction_type = request.GET.get("transaction_type", "")
    transactions = get_transaction_repository().list(
        transaction_type=transaction_type,
        date_from=date_from,
        date_to=date_to,
    )
    page = Paginator(transactions, PAGE_SIZE).get_page(request.GET.get("page"))
    context = {
        "page": page,
        "transaction_type": transaction_type,
        "date_from": date_from_value,
        "date_to": date_to_value,
        "total_count": len(transactions),
    }
    return render(request, "transactions/list.html", context)


def _parse_date(value: str | None) -> date | None:
    """Parse an ISO date query parameter."""
    try:
        return date.fromisoformat(value) if value else None
    except ValueError:
        return None
