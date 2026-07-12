from decimal import Decimal

from django.conf import settings
from django.db import models, transaction
from django.db.models import Count, Q, Sum
from django.utils import timezone

from audit.services import AuditService
from savings.models import ShareAccount, Transaction


class ShareAccountService:
    def ensure_account(self, user):
        account, _ = ShareAccount.objects.get_or_create(member=user)
        return account

    def list_accounts(self):
        return ShareAccount.objects.select_related(
            "member",
            "member__member_profile",
        )

    def get_member_summary(self, user):
        account = self.ensure_account(user)
        pending = account.transactions.filter(status=Transaction.Status.PENDING).count()
        return {
            "account_id": account.id,
            "balance": str(account.balance),
            "total_shares": str(account.total_shares),
            "share_value": settings.SHARE_VALUE,
            "pending_count": pending,
            "member_number": user.member_profile.member_number,
            "full_name": user.get_full_name(),
        }


class TransactionService:
    def __init__(self):
        self._audit = AuditService()
        self._accounts = ShareAccountService()

    def list_for_user(self, user, query_params=None):
        query_params = query_params or {}
        if user.is_member_user:
            qs = Transaction.objects.filter(account__member=user)
        else:
            qs = Transaction.objects.all()
            if member_id := query_params.get("member_id"):
                qs = qs.filter(account__member_id=member_id)
        if status_filter := query_params.get("status"):
            qs = qs.filter(status=status_filter)
        return qs.select_related(
            "account__member__member_profile",
            "submitted_by",
            "verified_by",
        )

    @transaction.atomic
    def submit_deposit(self, member_user, amount, reference="", notes=""):
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        account = self._accounts.ensure_account(member_user)
        txn = Transaction.objects.create(
            account=account,
            transaction_type=Transaction.Type.DEPOSIT,
            amount=amount,
            status=Transaction.Status.PENDING,
            reference=reference or "",
            notes=notes or "",
            submitted_by=member_user,
        )
        self._audit.log(
            "DEPOSIT_SUBMITTED",
            member_user.member_profile.member_number,
            f"Deposit {amount} pending (txn #{txn.id})",
        )
        return txn

    @transaction.atomic
    def verify(self, txn_id, treasurer):
        txn = (
            Transaction.objects.select_for_update()
            .select_related("account")
            .get(pk=txn_id)
        )
        if txn.status != Transaction.Status.PENDING:
            raise ValueError("Only pending transactions can be verified.")

        account = txn.account
        if txn.transaction_type == Transaction.Type.DEPOSIT:
            account.balance += txn.amount
        elif txn.transaction_type == Transaction.Type.WITHDRAWAL:
            if account.balance < txn.amount:
                raise ValueError("Insufficient balance for withdrawal.")
            account.balance -= txn.amount
        elif txn.transaction_type == Transaction.Type.ADJUSTMENT:
            account.balance += txn.amount

        share_value = Decimal(settings.SHARE_VALUE)
        account.total_shares = (
            (account.balance / share_value).quantize(Decimal("0.01"))
            if share_value
            else Decimal("0.00")
        )
        account.save(update_fields=["balance", "total_shares", "updated_at"])

        txn.status = Transaction.Status.VERIFIED
        txn.verified_by = treasurer
        txn.verified_at = timezone.now()
        txn.save(update_fields=["status", "verified_by", "verified_at"])

        self._audit.log(
            "DEPOSIT_VERIFIED",
            treasurer.username,
            f"Verified txn #{txn.id} amount={txn.amount}",
        )
        return txn

    @transaction.atomic
    def reject(self, txn_id, treasurer, reason=""):
        txn = Transaction.objects.select_for_update().get(pk=txn_id)
        if txn.status != Transaction.Status.PENDING:
            raise ValueError("Only pending transactions can be rejected.")
        txn.status = Transaction.Status.REJECTED
        txn.verified_by = treasurer
        txn.verified_at = timezone.now()
        txn.rejection_reason = reason or ""
        txn.save(
            update_fields=[
                "status",
                "verified_by",
                "verified_at",
                "rejection_reason",
            ]
        )
        self._audit.log(
            "DEPOSIT_REJECTED",
            treasurer.username,
            f"Rejected txn #{txn.id}: {reason}",
        )
        return txn


class DashboardService:
    def staff_stats(self):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        members = User.objects.filter(role=User.Role.MEMBER)
        aggregates = Transaction.objects.aggregate(
            pending=Count("id", filter=Q(status=Transaction.Status.PENDING)),
            verified_total=Sum(
                "amount",
                filter=Q(
                    status=Transaction.Status.VERIFIED,
                    transaction_type=Transaction.Type.DEPOSIT,
                ),
            ),
        )
        pool = ShareAccount.objects.aggregate(total=Sum("balance"))
        return {
            "members_total": members.count(),
            "members_verified": members.filter(is_verified=True).count(),
            "members_pending": members.filter(is_verified=False).count(),
            "pending_transactions": aggregates["pending"] or 0,
            "total_pool": str(pool["total"] or Decimal("0.00")),
            "verified_deposits_sum": str(aggregates["verified_total"] or Decimal("0.00")),
        }
