from django import forms

from apps.settings_app.models import AppSetting


class AppSettingForm(forms.ModelForm):
    class Meta:
        model = AppSetting
        fields = [
            "clinic_name",
            "queue_prefix",
            "public_display_show_patient_name",
            "urgent_cases_jump_queue",
            "daily_reset_mode",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = "w-full rounded border px-3 py-2"
            if isinstance(field.widget, forms.CheckboxInput):
                css = "rounded border-slate-300"
            field.widget.attrs["class"] = css
