from django.contrib.auth import get_user_model
from django.db import transaction

from accounts.models import MemberProfile
from audit.services import AuditService

User = get_user_model()


class AuthenticationService:
    def __init__(self):
        self._audit = AuditService()

    def authenticate_staff(self, username, password):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self._audit.log("LOGIN_FAILED", username, "Invalid staff credentials")
            return None, "Invalid credentials."

        if not user.check_password(password):
            self._audit.log("LOGIN_FAILED", username, "Wrong password")
            return None, "Invalid credentials."

        if not user.is_staff_user:
            self._audit.log("LOGIN_FAILED", username, "Not a staff account")
            return None, "This is not a staff account."

        if not user.is_active:
            self._audit.log("LOGIN_FAILED", username, "Account deactivated")
            return None, "This account has been deactivated."

        self._audit.log("LOGIN", username, "Staff login successful")
        return user, None

    def authenticate_member(self, member_number, password):
        try:
            profile = MemberProfile.objects.select_related("user").get(
                member_number=member_number
            )
        except MemberProfile.DoesNotExist:
            self._audit.log("LOGIN_FAILED", member_number, "Invalid member credentials")
            return None, "Invalid member number or password."

        user = profile.user

        if not user.check_password(password):
            self._audit.log("LOGIN_FAILED", member_number, "Invalid member credentials")
            return None, "Invalid member number or password."

        if not user.is_active:
            self._audit.log("LOGIN_FAILED", member_number, "Member deactivated")
            return None, "This member account has been deactivated."

        if not user.is_verified:
            self._audit.log("LOGIN_FAILED", member_number, "Member not verified")
            return None, "Your membership has not been verified yet."

        self._audit.log("LOGIN", member_number, "Member login successful")
        return user, None


class MemberRegistrationService:
    def __init__(self):
        self._audit = AuditService()

    @transaction.atomic
    def register(self, validated_data, auto_verify=False):
        from savings.services import ShareAccountService

        names = validated_data["full_name"].strip().split(" ", 1)
        user = User.objects.create_user(
            username=validated_data["email"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=names[0],
            last_name=names[1] if len(names) > 1 else "",
            role=User.Role.MEMBER,
            is_verified=auto_verify,
        )
        profile = MemberProfile.objects.create(
            user=user,
            national_id=validated_data["national_id"],
            phone=validated_data["phone"],
            address=validated_data.get("address", ""),
        )
        ShareAccountService().ensure_account(user)
        self._audit.log(
            "REGISTER_MEMBER",
            validated_data["full_name"],
            f"Member registered: {profile.member_number} (verified={auto_verify})",
        )
        return profile


class MemberManagementService:
    def __init__(self):
        self._audit = AuditService()

    def list_members(self, query_params=None):
        qs = (
            User.objects.filter(role=User.Role.MEMBER)
            .select_related("member_profile", "share_account")
        )
        query_params = query_params or {}
        if q := query_params.get("q"):
            qs = (
                qs.filter(first_name__icontains=q)
                | qs.filter(last_name__icontains=q)
                | qs.filter(member_profile__member_number__icontains=q)
                | qs.filter(member_profile__phone__icontains=q)
            )
        if query_params.get("verified") == "true":
            qs = qs.filter(is_verified=True)
        elif query_params.get("verified") == "false":
            qs = qs.filter(is_verified=False)
        return qs

    def verify(self, member_id, verified_by):
        user = User.objects.get(pk=member_id, role=User.Role.MEMBER)
        user.is_verified = True
        user.save(update_fields=["is_verified"])
        self._audit.log(
            "VERIFY_MEMBER",
            verified_by.username,
            f"Verified member: {user.get_full_name()}",
        )
        return user

    def deactivate(self, member_id, deactivated_by):
        user = User.objects.get(pk=member_id, role=User.Role.MEMBER)
        user.is_active = False
        user.save(update_fields=["is_active"])
        self._audit.log(
            "DEACTIVATE_MEMBER",
            deactivated_by.username,
            f"Deactivated member: {user.get_full_name()}",
        )
        return user


class StaffManagementService:
    def __init__(self):
        self._audit = AuditService()

    def list_staff(self):
        return User.objects.filter(role__in=User.STAFF_ROLES)

    @transaction.atomic
    def create_staff(self, validated_data, created_by):
        names = validated_data["full_name"].strip().split(" ", 1)
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=names[0],
            last_name=names[1] if len(names) > 1 else "",
            role=validated_data["role"],
            is_verified=True,
            is_staff=True,
        )
        self._audit.log(
            "CREATE_STAFF",
            created_by.username,
            f"Created staff: {user.username} ({user.role})",
        )
        return user

    def deactivate(self, staff_id, deactivated_by):
        user = User.objects.get(pk=staff_id)
        if user.role not in User.STAFF_ROLES:
            raise ValueError("Not a staff user.")
        if user.id == deactivated_by.id:
            raise ValueError("You cannot deactivate yourself.")
        user.is_active = False
        user.save(update_fields=["is_active"])
        self._audit.log(
            "DEACTIVATE_STAFF",
            deactivated_by.username,
            f"Deactivated staff: {user.username}",
        )
        return user
