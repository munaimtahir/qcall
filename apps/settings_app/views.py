from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from apps.accounts.decorators import role_required
from apps.queue.services import daily_reset
from apps.settings_app.forms import AppSettingForm
from apps.settings_app.services import get_app_settings


@role_required("admin",)
@require_http_methods(["GET", "POST"])
def settings_home(request):
    settings_obj = get_app_settings()
    if request.method == "POST":
        form = AppSettingForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Settings updated.")
            return redirect("settings_app:settings-home")
    else:
        form = AppSettingForm(instance=settings_obj)
    return render(request, "settings_app/settings.html", {"form": form})


@role_required("admin",)
@require_POST
def queue_reset(request):
    daily_reset()
    messages.success(request, "Today's queue has been reset and archived.")
    return redirect("settings_app:settings-home")
