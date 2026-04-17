from django.contrib import admin

from apps.patients.models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "mr_number", "mobile_number", "age", "gender", "updated_at")
    search_fields = ("full_name", "mobile_number", "mr_number")
    list_filter = ("gender",)

