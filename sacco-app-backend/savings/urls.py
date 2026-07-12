from django.urls import path

from savings.views import (
    AccountListView,
    DashboardView,
    MySavingsView,
    TransactionListCreateView,
    TransactionRejectView,
    TransactionVerifyView,
)

urlpatterns = [
    path("me/", MySavingsView.as_view()),
    path("accounts/", AccountListView.as_view()),
    path("transactions/", TransactionListCreateView.as_view()),
    path("transactions/<int:txn_id>/verify/", TransactionVerifyView.as_view()),
    path("transactions/<int:txn_id>/reject/", TransactionRejectView.as_view()),
    path("dashboard/", DashboardView.as_view()),
]
