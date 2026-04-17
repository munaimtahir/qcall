from django.contrib import admin

from apps.settings_app.models import AppSetting


@admin.register(AppSetting)
class AppSettingAdmin(admin.ModelAdmin):
    list_display = ("clinic_name", "urgent_cases_jump_queue", "daily_reset_mode", "updated_at")

