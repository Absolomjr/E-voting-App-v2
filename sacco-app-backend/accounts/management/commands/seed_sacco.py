from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import MemberProfile
from savings.services import ShareAccountService

User = get_user_model()


class Command(BaseCommand):
    help = "Seed demo SACCO admin, treasurer, and one verified member."

    @transaction.atomic
    def handle(self, *args, **options):
        admin, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@sacco.local",
                "first_name": "System",
                "last_name": "Admin",
                "role": User.Role.SUPER_ADMIN,
                "is_verified": True,
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            admin.set_password("admin123")
            admin.save()
            self.stdout.write(self.style.SUCCESS("Created admin / admin123"))
        else:
            self.stdout.write("Admin already exists")

        treasurer, created = User.objects.get_or_create(
            username="treasurer",
            defaults={
                "email": "treasurer@sacco.local",
                "first_name": "Group",
                "last_name": "Treasurer",
                "role": User.Role.TREASURER,
                "is_verified": True,
                "is_staff": True,
            },
        )
        if created:
            treasurer.set_password("treasurer123")
            treasurer.save()
            self.stdout.write(self.style.SUCCESS("Created treasurer / treasurer123"))
        else:
            self.stdout.write("Treasurer already exists")

        member_user, created = User.objects.get_or_create(
            username="member@sacco.local",
            defaults={
                "email": "member@sacco.local",
                "first_name": "Demo",
                "last_name": "Member",
                "role": User.Role.MEMBER,
                "is_verified": True,
            },
        )
        if created:
            member_user.set_password("member123")
            member_user.save()
            profile = MemberProfile.objects.create(
                user=member_user,
                member_number="SACCO0001",
                national_id="NID-DEMO-001",
                phone="+256700000001",
                address="Kampala",
            )
            ShareAccountService().ensure_account(member_user)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Created member {profile.member_number} / member123"
                )
            )
        else:
            self.stdout.write("Demo member already exists")

        self.stdout.write(self.style.SUCCESS("Seed complete."))
