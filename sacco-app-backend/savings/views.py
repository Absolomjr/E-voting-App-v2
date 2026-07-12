from savings.models import Transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsStaffUser, IsTreasurer, IsVerifiedMember
from savings.serializers import (
    DepositCreateSerializer,
    RejectSerializer,
    ShareAccountSerializer,
    TransactionSerializer,
)
from savings.services import DashboardService, ShareAccountService, TransactionService


class MySavingsView(APIView):
    permission_classes = [IsVerifiedMember]

    def get(self, request):
        return Response(ShareAccountService().get_member_summary(request.user))


class AccountListView(APIView):
    permission_classes = [IsStaffUser]

    def get(self, request):
        qs = ShareAccountService().list_accounts()
        return Response(ShareAccountSerializer(qs, many=True).data)


class TransactionListCreateView(APIView):
    def get_permissions(self):
        from rest_framework.permissions import IsAuthenticated

        if self.request.method == "POST":
            return [IsVerifiedMember()]
        return [IsAuthenticated()]

    def get(self, request):
        user = request.user
        if user.is_member_user:
            if not user.is_verified:
                return Response({"detail": "Not verified."}, status=status.HTTP_403_FORBIDDEN)
        elif not user.is_staff_user:
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)

        qs = TransactionService().list_for_user(user, request.query_params)
        return Response(TransactionSerializer(qs[:100], many=True).data)

    def post(self, request):
        serializer = DepositCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            txn = TransactionService().submit_deposit(
                request.user,
                serializer.validated_data["amount"],
                serializer.validated_data.get("reference", ""),
                serializer.validated_data.get("notes", ""),
            )
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(TransactionSerializer(txn).data, status=status.HTTP_201_CREATED)


class TransactionVerifyView(APIView):
    permission_classes = [IsTreasurer]

    def post(self, request, txn_id):
        try:
            txn = TransactionService().verify(txn_id, request.user)
        except Transaction.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(TransactionSerializer(txn).data)


class TransactionRejectView(APIView):
    permission_classes = [IsTreasurer]

    def post(self, request, txn_id):
        serializer = RejectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            txn = TransactionService().reject(
                txn_id,
                request.user,
                serializer.validated_data.get("reason", ""),
            )
        except Transaction.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(TransactionSerializer(txn).data)


class DashboardView(APIView):
    permission_classes = [IsStaffUser]

    def get(self, request):
        return Response(DashboardService().staff_stats())
