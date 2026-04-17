from django.urls import path

from apps.queue import views

app_name = "queue"

urlpatterns = [
    path("add/", views.add_new_patient_to_queue, name="add"),
    path("add-existing/", views.add_existing_patient_to_queue, name="add-existing"),
    path("call-next/", views.call_next, name="call-next"),
    path("<int:visit_id>/done/", views.mark_done, name="done"),
    path("<int:visit_id>/skip/", views.skip, name="skip"),
    path("<int:visit_id>/cancel/", views.cancel, name="cancel"),
    path("<int:visit_id>/requeue/", views.requeue, name="requeue"),
    path("<int:visit_id>/urgent/", views.urgent, name="urgent"),
    path("partials/list/", views.queue_list_partial, name="partial-list"),
    path("partials/current/", views.queue_current_partial, name="partial-current"),
]
