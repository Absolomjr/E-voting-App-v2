from audit.models import AuditLog


class AuditService:
    def log(self, action, user_identifier, details=""):
        return AuditLog.objects.create(
            action=action,
            user_identifier=str(user_identifier)[:200],
            details=details or "",
        )

    def list_logs(self, query_params=None):
        qs = AuditLog.objects.all()
        query_params = query_params or {}
        if action := query_params.get("action"):
            qs = qs.filter(action=action)
        if user := query_params.get("user"):
            qs = qs.filter(user_identifier__icontains=user)
        return qs

    def action_types(self):
        return (
            AuditLog.objects.order_by("action")
            .values_list("action", flat=True)
            .distinct()
        )
