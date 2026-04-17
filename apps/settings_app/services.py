from apps.settings_app.models import AppSetting


def get_app_settings() -> AppSetting:
    settings_obj, _ = AppSetting.objects.get_or_create(pk=1)
    return settings_obj

