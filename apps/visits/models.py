from django.conf import settings
from django.db import models
from django.db.models import Q


class VisitStatus(models.TextChoices):
    WAITING = "waiting", "Waiting"
    WITH_DOCTOR = "with_doctor", "With Doctor"
    COMPLETED = "completed", "Completed"
    SKIPPED = "skipped", "Skipped"
    CANCELLED = "cancelled", "Cancelled"
    NO_SHOW = "no_show", "No Show"


class VisitPriority(models.TextChoices):
    NORMAL = "normal", "Normal"
    URGENT = "urgent", "Urgent"


class Visit(models.Model):
    patient = models.ForeignKey("patients.Patient", on_delete=models.PROTECT, related_name="visits")
    queue_session = models.ForeignKey("queue.DailyQueueSession", on_delete=models.PROTECT, related_name="visits")
    token_number = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=VisitStatus.choices, default=VisitStatus.WAITING, db_index=True)
    priority_level = models.CharField(max_length=20, choices=VisitPriority.choices, default=VisitPriority.NORMAL, db_index=True)
    short_note = models.CharField(max_length=255, blank=True)
    doctor_note = models.TextField(blank=True)
    called_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="created_visits")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["queue_session", "token_number"], name="unique_token_per_queue_session"),
            models.UniqueConstraint(
                fields=["queue_session"],
                condition=Q(status=VisitStatus.WITH_DOCTOR),
                name="unique_with_doctor_per_session",
            ),
        ]
        ordering = ["token_number"]

    def __str__(self) -> str:
        return f"#{self.token_number} {self.patient.full_name}"

