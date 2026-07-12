from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.models import MemberProfile

User = get_user_model()


class StaffLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class MemberLoginSerializer(serializers.Serializer):
    member_number = serializers.CharField()
    password = serializers.CharField(write_only=True)


class MemberRegistrationSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, write_only=True)
    national_id = serializers.CharField(max_length=50)
    phone = serializers.CharField(max_length=20)
    address = serializers.CharField(required=False, allow_blank=True, default="")

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value.lower()

    def validate_national_id(self, value):
        if MemberProfile.objects.filter(national_id=value).exists():
            raise serializers.ValidationError("National ID already registered.")
        return value


class MemberCreateSerializer(serializers.Serializer):
    """Staff-created member (auto-verified)."""

    full_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, write_only=True)
    national_id = serializers.CharField(max_length=50)
    phone = serializers.CharField(max_length=20)
    address = serializers.CharField(required=False, allow_blank=True, default="")


class StaffCreateSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=150)
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, write_only=True)
    role = serializers.ChoiceField(
        choices=[
            User.Role.TREASURER,
            User.Role.SECRETARY,
            User.Role.SUPER_ADMIN,
        ]
    )


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(min_length=6, write_only=True)


class MemberListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    member_number = serializers.CharField(source="member_profile.member_number")
    phone = serializers.CharField(source="member_profile.phone")
    national_id = serializers.CharField(source="member_profile.national_id")
    join_date = serializers.DateField(source="member_profile.join_date")
    balance = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "email",
            "member_number",
            "phone",
            "national_id",
            "join_date",
            "is_verified",
            "is_active",
            "balance",
            "date_joined",
        ]

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_balance(self, obj):
        account = getattr(obj, "share_account", None)
        if account is None:
            return "0.00"
        return str(account.balance)


class StaffListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "full_name",
            "email",
            "role",
            "is_active",
            "date_joined",
        ]

    def get_full_name(self, obj):
        return obj.get_full_name()


class ProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField()
    email = serializers.EmailField()
    role = serializers.CharField()
    username = serializers.CharField(required=False, allow_null=True)
    member_number = serializers.CharField(required=False, allow_null=True)
    phone = serializers.CharField(required=False, allow_null=True)
    is_verified = serializers.BooleanField()
