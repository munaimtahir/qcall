from django.urls import path

from apps.patients import views

app_name = "patients"

urlpatterns = [
    path("", views.patient_list, name="list"),
    path("search/", views.patient_search_partial, name="search"),
    path("<int:pk>/", views.patient_detail, name="detail"),
]
