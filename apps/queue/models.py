from django.db import models
from django.db.models import Q


class DailyQueueSession(models.Model):
    queue_date = models.DateField(db_index=True)
    is_active = models.BooleanField(default=True)
    start_token_number = models.PositiveIntegerField(default=1)
    last_issued_token_number = models.PositiveIntegerField(default=0)
    current_visit = models.ForeignKey(
        "visits.Visit",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="current_for_sessions",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["queue_date"],
                condition=Q(is_active=True),
                name="unique_active_queue_session_per_date",
            )
        ]
        ordering = ["-queue_date", "-created_at"]

    def __str__(self) -> str:
        return f"{self.queue_date} ({'active' if self.is_active else 'closed'})"

