from django import forms

from apps.patients.models import Patient
from apps.visits.models import VisitPriority


class NewPatientToQueueForm(forms.Form):
    mr_number = forms.CharField(required=False, max_length=64)
    full_name = forms.CharField(max_length=255)
    mobile_number = forms.CharField(max_length=20)
    age = forms.IntegerField(min_value=0, max_value=130)
    gender = forms.ChoiceField(choices=[("male", "Male"), ("female", "Female"), ("other", "Other")])
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 2}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 2}))
    priority = forms.ChoiceField(choices=VisitPriority.choices, initial=VisitPriority.NORMAL)
    short_note = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 2}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = "w-full rounded border px-3 py-2"
            if isinstance(field.widget, forms.CheckboxInput):
                css = "rounded border-slate-300"
            field.widget.attrs["class"] = css

    def clean_mr_number(self):
        mr_number = self.cleaned_data.get("mr_number", "").strip()
        if mr_number and Patient.objects.filter(mr_number=mr_number).exists():
            raise forms.ValidationError("MR number already exists.")
        return mr_number


class AddExistingPatientToQueueForm(forms.Form):
    patient_id = forms.IntegerField(min_value=1)
    priority = forms.ChoiceField(choices=VisitPriority.choices, initial=VisitPriority.NORMAL)
    short_note = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "w-full rounded border px-3 py-2"
