from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from accounts.models import MemberProfile, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("username", "email", "role", "is_verified", "is_active")
    list_filter = ("role", "is_verified", "is_active")
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("SACCO", {"fields": ("role", "is_verified")}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ("SACCO", {"fields": ("role", "is_verified")}),
    )


@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ("member_number", "user", "phone", "national_id", "join_date")
    search_fields = ("member_number", "phone", "national_id", "user__username")
