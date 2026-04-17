from django.core.management.base import BaseCommand

from apps.accounts.models import User, UserRole


class Command(BaseCommand):
    help = "Create initial admin, reception, and doctor users if they do not exist."

    def handle(self, *args, **options):
        defaults = [
            {
                "username": "admin",
                "full_name": "System Admin",
                "role": UserRole.ADMIN,
                "is_staff": True,
                "is_superuser": True,
                "password": "admin123",
            },
            {
                "username": "reception1",
                "full_name": "Reception User",
                "role": UserRole.RECEPTION,
                "is_staff": True,
                "is_superuser": False,
                "password": "reception123",
            },
            {
                "username": "doctor1",
                "full_name": "Doctor User",
                "role": UserRole.DOCTOR,
                "is_staff": True,
                "is_superuser": False,
                "password": "doctor123",
            },
        ]
        for user_data in defaults:
            password = user_data.pop("password")
            user, created = User.objects.get_or_create(username=user_data["username"], defaults=user_data)
            if created:
                user.set_password(password)
                user.save(update_fields=["password"])
                self.stdout.write(self.style.SUCCESS(f"Created user: {user.username}"))
            else:
                self.stdout.write(f"User exists: {user.username}")
