"""URL configuration for transaction views."""

from django.urls import path

from .views import transaction_list

urlpatterns = [path("", transaction_list, name="transaction-list")]
