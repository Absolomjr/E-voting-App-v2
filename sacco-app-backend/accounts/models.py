import random
import string

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    class Role(models.TextChoices):
        SUPER_ADMIN = "super_admin", "Super Admin"
        TREASURER = "treasurer", "Treasurer"
        SECRETARY = "secretary", "Secretary"
        MEMBER = "member", "Member"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MEMBER,
        db_index=True,
    )
    is_verified = models.BooleanField(default=False)

    STAFF_ROLES = {
        Role.SUPER_ADMIN,
        Role.TREASURER,
        Role.SECRETARY,
    }

    @property
    def is_staff_user(self):
        return self.role in self.STAFF_ROLES

    @property
    def is_member_user(self):
        return self.role == self.Role.MEMBER

    @property
    def is_super_admin(self):
        return self.role == self.Role.SUPER_ADMIN

    @property
    def is_treasurer(self):
        return self.role in {self.Role.TREASURER, self.Role.SUPER_ADMIN}

    @property
    def can_manage_members(self):
        return self.role in {
            self.Role.SUPER_ADMIN,
            self.Role.SECRETARY,
        }

    class Meta:
        ordering = ["-date_joined"]

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"


class MemberProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="member_profile",
    )
    member_number = models.CharField(max_length=16, unique=True, editable=False, db_index=True)
    national_id = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    join_date = models.DateField(default=timezone.localdate)

    def save(self, *args, **kwargs):
        if not self.member_number:
            self.member_number = self._generate_member_number()
        super().save(*args, **kwargs)

    @staticmethod
    def _generate_member_number():
        while True:
            suffix = "".join(random.choices(string.digits, k=4))
            number = f"SACCO{suffix}"
            if not MemberProfile.objects.filter(member_number=number).exists():
                return number

    class Meta:
        ordering = ["-join_date"]

    def __str__(self):
        return f"{self.user.get_full_name()} [{self.member_number}]"
