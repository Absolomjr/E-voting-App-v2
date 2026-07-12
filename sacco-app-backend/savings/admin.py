from django.contrib import admin

from savings.models import ShareAccount, Transaction


@admin.register(ShareAccount)
class ShareAccountAdmin(admin.ModelAdmin):
    list_display = ("id", "member", "balance", "total_shares", "updated_at")
    search_fields = ("member__username", "member__member_profile__member_number")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "account",
        "transaction_type",
        "amount",
        "status",
        "created_at",
    )
    list_filter = ("status", "transaction_type")
    search_fields = ("reference", "account__member__username")
