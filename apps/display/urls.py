from django.urls import path

from apps.display import views

app_name = "display"

urlpatterns = [
    path("", views.display_screen, name="screen"),
    path("partials/panel/", views.display_panel_partial, name="partial-panel"),
]
