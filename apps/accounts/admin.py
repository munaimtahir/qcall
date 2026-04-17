from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from apps.accounts.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        (
            "Clinic Role",
            {"fields": ("full_name", "role", "created_at", "updated_at")},
        ),
    )
    readonly_fields = ("created_at", "updated_at")
    list_display = ("username", "full_name", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
