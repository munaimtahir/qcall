from django.contrib import admin

from apps.queue.models import DailyQueueSession


@admin.register(DailyQueueSession)
class DailyQueueSessionAdmin(admin.ModelAdmin):
    list_display = ("queue_date", "is_active", "start_token_number", "last_issued_token_number", "current_visit")
    list_filter = ("is_active", "queue_date")
