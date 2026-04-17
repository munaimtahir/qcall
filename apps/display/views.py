from django.shortcuts import render

from apps.queue.services import get_or_create_active_session, waiting_queryset
from apps.visits.models import VisitStatus


def _display_context():
    session = get_or_create_active_session()
    current = session.current_visit
    if current and current.status != VisitStatus.WITH_DOCTOR:
        current = None
    next_visits = waiting_queryset(session).select_related("patient")[:5]
    return {"session": session, "current_visit": current, "next_visits": next_visits}


def display_screen(request):
    return render(request, "display/screen.html", _display_context())


def display_panel_partial(request):
    return render(request, "display/partials/_panel.html", _display_context())

