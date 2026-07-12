from decimal import Decimal

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ShareAccount",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("balance", models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=14)),
                ("total_shares", models.DecimalField(decimal_places=2, default=Decimal("0.00"), help_text="Shares owned (balance / share value).", max_digits=14)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("member", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="share_account", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-updated_at"]},
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("transaction_type", models.CharField(choices=[("deposit", "Deposit"), ("withdrawal", "Withdrawal"), ("adjustment", "Adjustment")], db_index=True, max_length=20)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=14)),
                ("status", models.CharField(choices=[("pending", "Pending"), ("verified", "Verified"), ("rejected", "Rejected")], db_index=True, default="pending", max_length=20)),
                ("reference", models.CharField(blank=True, max_length=64)),
                ("notes", models.TextField(blank=True)),
                ("rejection_reason", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("verified_at", models.DateTimeField(blank=True, null=True)),
                ("account", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="transactions", to="savings.shareaccount")),
                ("submitted_by", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="submitted_transactions", to=settings.AUTH_USER_MODEL)),
                ("verified_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="verified_transactions", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddIndex(
            model_name="transaction",
            index=models.Index(fields=["status", "created_at"], name="savings_tra_status_7f2c0a_idx"),
        ),
        migrations.AddIndex(
            model_name="transaction",
            index=models.Index(fields=["account", "status"], name="savings_tra_account_8a1b2c_idx"),
        ),
    ]
