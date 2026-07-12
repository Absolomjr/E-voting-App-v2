from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsSuperAdmin, IsStaffUser
from audit.serializers import AuditLogSerializer
from audit.services import AuditService


class AuditLogListView(APIView):
    permission_classes = [IsStaffUser]

    def get(self, request):
        # Treasurers/secretaries can view; mutations are never exposed here
        if request.user.role not in {
            request.user.Role.SUPER_ADMIN,
            request.user.Role.TREASURER,
            request.user.Role.SECRETARY,
        }:
            return Response({"detail": "Forbidden."}, status=403)
        qs = AuditService().list_logs(request.query_params)[:200]
        return Response(AuditLogSerializer(qs, many=True).data)


class AuditActionTypesView(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self, request):
        return Response(list(AuditService().action_types()))
