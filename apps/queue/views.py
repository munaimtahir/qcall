from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from apps.accounts.decorators import role_required
from apps.patients.models import Patient
from apps.queue.forms import AddExistingPatientToQueueForm, NewPatientToQueueForm
from apps.queue.services import (
    call_next_patient,
    cancel_visit,
    daily_reset,
    enqueue_patient,
    get_or_create_active_session,
    mark_urgent,
    mark_visit_done,
    queue_list_queryset,
    requeue_visit,
    skip_visit,
    waiting_queryset,
)
from apps.visits.models import Visit, VisitStatus


def _queue_partial_context():
    session = get_or_create_active_session()
    return {"session": session, "queue_visits": queue_list_queryset(session)}


def _doctor_panel_context():
    session = get_or_create_active_session()
    current = session.current_visit
    if current and current.status != VisitStatus.WITH_DOCTOR:
        current = None
    next_visits = waiting_queryset(session).select_related("patient")[:8]
    history = []
    if current:
        history = (
            Visit.objects.filter(patient=current.patient)
            .exclude(pk=current.pk)
            .order_by("-created_at")[:5]
        )
    return {"session": session, "current_visit": current, "next_visits": next_visits, "history_visits": history}


@role_required("reception", "admin")
def reception_dashboard(request):
    context = _queue_partial_context()
    context["new_patient_form"] = NewPatientToQueueForm()
    context["existing_patient_form"] = AddExistingPatientToQueueForm()
    return render(request, "reception/dashboard.html", context)


@role_required("doctor", "admin")
def doctor_dashboard(request):
    return render(request, "doctor/dashboard.html", _doctor_panel_context())


@role_required("reception", "doctor", "admin")
@require_GET
def queue_list_partial(request):
    return render(request, "queue/partials/_queue_list.html", _queue_partial_context())


@role_required("doctor", "admin")
@require_GET
def queue_current_partial(request):
    return render(request, "doctor/partials/_doctor_panels.html", _doctor_panel_context())


@role_required("reception", "admin")
@require_POST
def add_new_patient_to_queue(request):
    form = NewPatientToQueueForm(request.POST)
    if form.is_valid():
        with transaction.atomic():
            patient = Patient.objects.create(
                mr_number=form.cleaned_data["mr_number"] or None,
                full_name=form.cleaned_data["full_name"],
                mobile_number=form.cleaned_data["mobile_number"],
                age=form.cleaned_data["age"],
                gender=form.cleaned_data["gender"],
                address=form.cleaned_data["address"],
                notes=form.cleaned_data["notes"],
            )
            enqueue_patient(
                patient=patient,
                created_by=request.user,
                priority=form.cleaned_data["priority"],
                short_note=form.cleaned_data["short_note"],
            )
        messages.success(request, "Patient added to queue.")
    else:
        messages.error(request, "Could not add patient. Please check the form values.")
    return render(request, "queue/partials/_queue_list.html", _queue_partial_context())


@role_required("reception", "admin")
@require_POST
def add_existing_patient_to_queue(request):
    form = AddExistingPatientToQueueForm(request.POST)
    if form.is_valid():
        patient = get_object_or_404(Patient, pk=form.cleaned_data["patient_id"])
        enqueue_patient(
            patient=patient,
            created_by=request.user,
            priority=form.cleaned_data["priority"],
            short_note=form.cleaned_data["short_note"],
        )
        messages.success(request, "Existing patient added to queue.")
    else:
        messages.error(request, "Could not add existing patient to queue.")
    return render(request, "queue/partials/_queue_list.html", _queue_partial_context())


@role_required("doctor", "admin")
@require_POST
def call_next(request):
    call_next_patient(acted_by=request.user)
    return render(request, "doctor/partials/_doctor_panels.html", _doctor_panel_context())


@role_required("doctor", "admin")
@require_POST
def mark_done(request, visit_id: int):
    visit = get_object_or_404(Visit, pk=visit_id)
    try:
        mark_visit_done(visit, acted_by=request.user)
    except ValueError as exc:
        messages.error(request, str(exc))
    return render(request, "doctor/partials/_doctor_panels.html", _doctor_panel_context())


@role_required("doctor", "reception", "admin")
@require_POST
def skip(request, visit_id: int):
    visit = get_object_or_404(Visit, pk=visit_id)
    try:
        skip_visit(visit, acted_by=request.user)
    except ValueError as exc:
        messages.error(request, str(exc))
    target = request.POST.get("target", "queue")
    if target == "doctor":
        return render(request, "doctor/partials/_doctor_panels.html", _doctor_panel_context())
    return render(request, "queue/partials/_queue_list.html", _queue_partial_context())


@role_required("reception", "admin")
@require_POST
def cancel(request, visit_id: int):
    visit = get_object_or_404(Visit, pk=visit_id)
    try:
        cancel_visit(visit, acted_by=request.user)
    except ValueError as exc:
        messages.error(request, str(exc))
    return render(request, "queue/partials/_queue_list.html", _queue_partial_context())


@role_required("reception", "admin")
@require_POST
def requeue(request, visit_id: int):
    visit = get_object_or_404(Visit, pk=visit_id)
    try:
        requeue_visit(visit, acted_by=request.user)
    except ValueError as exc:
        messages.error(request, str(exc))
    return render(request, "queue/partials/_queue_list.html", _queue_partial_context())


@role_required("reception", "admin")
@require_POST
def urgent(request, visit_id: int):
    visit = get_object_or_404(Visit, pk=visit_id)
    try:
        mark_urgent(visit, acted_by=request.user)
    except ValueError as exc:
        messages.error(request, str(exc))
    return render(request, "queue/partials/_queue_list.html", _queue_partial_context())


@role_required("admin",)
@require_POST
def reset_today_queue(request):
    daily_reset()
    messages.success(request, "Today's queue has been reset and archived.")
    return redirect("settings_app:settings-home")
