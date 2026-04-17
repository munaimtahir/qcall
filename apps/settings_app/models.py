from django.db import models


class DailyResetMode(models.TextChoices):
    MANUAL = "manual", "Manual"
    AUTO = "auto", "Auto"


class AppSetting(models.Model):
    clinic_name = models.CharField(max_length=255, default="Queue Management MVP")
    queue_prefix = models.CharField(max_length=20, blank=True)
    public_display_show_patient_name = models.BooleanField(default=False)
    urgent_cases_jump_queue = models.BooleanField(default=True)
    daily_reset_mode = models.CharField(max_length=20, choices=DailyResetMode.choices, default=DailyResetMode.MANUAL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "App Setting"
        verbose_name_plural = "App Settings"

    def __str__(self) -> str:
        return self.clinic_name

