from rest_framework.permissions import BasePermission


class IsStaffUser(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_staff_user
        )


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_super_admin
        )


class IsTreasurer(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_treasurer
        )


class IsMemberManager(BasePermission):
    """Super admin or secretary — can manage members."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.can_manage_members
        )


class IsVerifiedMember(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_member_user
            and request.user.is_verified
        )
