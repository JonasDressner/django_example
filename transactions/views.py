from datetime import date

from django.core.paginator import Paginator
from django.shortcuts import render

from .services import get_transaction_repository


def transaction_list(request):
    date_from = _parse_date(request.GET.get("date_from"))
    date_to = _parse_date(request.GET.get("date_to"))
    transaction_type = request.GET.get("transaction_type", "")
    transactions = get_transaction_repository().list(
        transaction_type=transaction_type,
        date_from=date_from,
        date_to=date_to,
    )
    page = Paginator(transactions, 10).get_page(request.GET.get("page"))
    context = {
        "page": page,
        "transaction_type": transaction_type,
        "date_from": request.GET.get("date_from", ""),
        "date_to": request.GET.get("date_to", ""),
        "total_count": len(transactions),
    }
    return render(request, "transactions/list.html", context)


def _parse_date(value):
    try:
        return date.fromisoformat(value) if value else None
    except ValueError:
        return None
