from django.db import models


class GenderChoice(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"
    OTHER = "other", "Other"


class Patient(models.Model):
    mr_number = models.CharField(max_length=64, blank=True, null=True, unique=True)
    full_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=20, db_index=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=20, choices=GenderChoice.choices)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self) -> str:
        return f"{self.full_name} ({self.mobile_number})"

