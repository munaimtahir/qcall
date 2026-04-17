from django.contrib import admin

from apps.visits.models import Visit


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ("id", "token_number", "patient", "status", "priority_level", "queue_session", "created_at")
    search_fields = ("patient__full_name", "patient__mobile_number", "patient__mr_number")
    list_filter = ("status", "priority_level", "queue_session__queue_date")

