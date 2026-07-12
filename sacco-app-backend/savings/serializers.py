from decimal import Decimal

from rest_framework import serializers

from savings.models import ShareAccount, Transaction


class DepositCreateSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=14, decimal_places=2, min_value=Decimal("0.01"))
    reference = serializers.CharField(required=False, allow_blank=True, max_length=64)
    notes = serializers.CharField(required=False, allow_blank=True)


class RejectSerializer(serializers.Serializer):
    reason = serializers.CharField(required=False, allow_blank=True)


class TransactionSerializer(serializers.ModelSerializer):
    member_name = serializers.SerializerMethodField()
    member_number = serializers.SerializerMethodField()
    submitted_by_name = serializers.SerializerMethodField()
    verified_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            "id",
            "transaction_type",
            "amount",
            "status",
            "reference",
            "notes",
            "rejection_reason",
            "member_name",
            "member_number",
            "submitted_by_name",
            "verified_by_name",
            "created_at",
            "verified_at",
        ]

    def get_member_name(self, obj):
        return obj.account.member.get_full_name()

    def get_member_number(self, obj):
        profile = getattr(obj.account.member, "member_profile", None)
        return profile.member_number if profile else None

    def get_submitted_by_name(self, obj):
        return obj.submitted_by.get_full_name() or obj.submitted_by.username

    def get_verified_by_name(self, obj):
        if not obj.verified_by:
            return None
        return obj.verified_by.get_full_name() or obj.verified_by.username


class ShareAccountSerializer(serializers.ModelSerializer):
    member_name = serializers.SerializerMethodField()
    member_number = serializers.SerializerMethodField()
    email = serializers.EmailField(source="member.email")

    class Meta:
        model = ShareAccount
        fields = [
            "id",
            "member_name",
            "member_number",
            "email",
            "balance",
            "total_shares",
            "updated_at",
        ]

    def get_member_name(self, obj):
        return obj.member.get_full_name()

    def get_member_number(self, obj):
        profile = getattr(obj.member, "member_profile", None)
        return profile.member_number if profile else None
