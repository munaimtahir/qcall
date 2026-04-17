from django import forms

from apps.patients.models import Patient


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ["mr_number", "full_name", "mobile_number", "age", "gender", "address", "notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 2}),
            "address": forms.Textarea(attrs={"rows": 2}),
        }

