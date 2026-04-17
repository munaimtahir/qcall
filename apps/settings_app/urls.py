from django.urls import path

from apps.settings_app import views

app_name = "settings_app"

urlpatterns = [
    path("", views.settings_home, name="settings-home"),
    path("queue/reset/", views.queue_reset, name="queue-reset"),
]
