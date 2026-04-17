from apps.settings_app.services import get_app_settings


def app_settings(request):
    return {"app_settings": get_app_settings()}

