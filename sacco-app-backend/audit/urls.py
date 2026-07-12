from django.urls import path

from audit.views import AuditActionTypesView, AuditLogListView

urlpatterns = [
    path("logs/", AuditLogListView.as_view()),
    path("actions/", AuditActionTypesView.as_view()),
]
