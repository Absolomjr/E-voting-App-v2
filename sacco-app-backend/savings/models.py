from decimal import Decimal

from django.conf import settings
from django.db import models


class ShareAccount(models.Model):
    member = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="share_account",
    )
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    total_shares = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Shares owned (balance / share value).",
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"Account<{self.member_id}> balance={self.balance}"


class Transaction(models.Model):
    class Type(models.TextChoices):
        DEPOSIT = "deposit", "Deposit"
        WITHDRAWAL = "withdrawal", "Withdrawal"
        ADJUSTMENT = "adjustment", "Adjustment"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        VERIFIED = "verified", "Verified"
        REJECTED = "rejected", "Rejected"

    account = models.ForeignKey(
        ShareAccount,
        on_delete=models.CASCADE,
        related_name="transactions",
    )
    transaction_type = models.CharField(max_length=20, choices=Type.choices, db_index=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )
    reference = models.CharField(max_length=64, blank=True)
    notes = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="submitted_transactions",
    )
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_transactions",
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "created_at"]),
            models.Index(fields=["account", "status"]),
        ]

    def __str__(self):
        return f"{self.transaction_type} {self.amount} [{self.status}]"
