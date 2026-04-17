from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from apps.queue import views as queue_views
from config import views as config_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.accounts.urls")),
    path("reception/", queue_views.reception_dashboard, name="reception-dashboard"),
    path("doctor/", queue_views.doctor_dashboard, name="doctor-dashboard"),
    path("patients/", include("apps.patients.urls")),
    path("queue/", include("apps.queue.urls")),
    path("display/", include("apps.display.urls")),
    path("settings/", include("apps.settings_app.urls")),
    path("service-worker.js", config_views.service_worker, name="pwa-service-worker"),
    path("manifest.webmanifest", RedirectView.as_view(url=settings.STATIC_URL + "manifest.webmanifest"), name="pwa-manifest"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
