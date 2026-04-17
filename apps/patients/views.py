from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from apps.accounts.decorators import role_required
from apps.patients.models import Patient
from apps.queue.forms import AddExistingPatientToQueueForm
from apps.visits.models import Visit


def _search_queryset(query: str):
    if not query:
        return Patient.objects.none()
    return Patient.objects.filter(
        Q(full_name__icontains=query) | Q(mobile_number__icontains=query) | Q(mr_number__icontains=query)
    ).order_by("full_name")[:20]


@role_required("reception", "doctor", "admin")
def patient_list(request):
    query = request.GET.get("q", "").strip()
    patients = _search_queryset(query) if query else Patient.objects.all().order_by("-updated_at")[:30]
    return render(request, "patients/list.html", {"patients": patients, "query": query})


@role_required("reception", "doctor", "admin")
def patient_detail(request, pk: int):
    patient = get_object_or_404(Patient, pk=pk)
    visits = Visit.objects.filter(patient=patient).select_related("queue_session").order_by("-created_at")
    return render(request, "patients/detail.html", {"patient": patient, "visits": visits})


@role_required("reception", "doctor", "admin")
def patient_search_partial(request):
    query = request.GET.get("q", "").strip()
    patients = _search_queryset(query)
    form = AddExistingPatientToQueueForm()
    return render(
        request,
        "patients/partials/_search_results.html",
        {"patients": patients, "query": query, "queue_form": form},
    )

