from datetime import date

from django.db import transaction
from django.db.models import Case, IntegerField, Value, When
from django.utils import timezone

from apps.patients.models import Patient
from apps.queue.models import DailyQueueSession
from apps.settings_app.services import get_app_settings
from apps.visits.models import Visit, VisitPriority, VisitStatus


def get_or_create_active_session(for_date: date | None = None) -> DailyQueueSession:
    queue_date = for_date or timezone.localdate()
    session = DailyQueueSession.objects.filter(queue_date=queue_date, is_active=True).first()
    if session:
        return session
    return DailyQueueSession.objects.create(queue_date=queue_date, is_active=True, start_token_number=1, last_issued_token_number=0)


@transaction.atomic
def issue_next_token(queue_session: DailyQueueSession) -> int:
    session = DailyQueueSession.objects.select_for_update().get(pk=queue_session.pk)
    next_token = max(session.start_token_number, session.last_issued_token_number + 1)
    session.last_issued_token_number = next_token
    session.save(update_fields=["last_issued_token_number", "updated_at"])
    return next_token


@transaction.atomic
def enqueue_patient(
    *,
    patient: Patient,
    created_by,
    priority: str = VisitPriority.NORMAL,
    short_note: str = "",
) -> Visit:
    queue_session = get_or_create_active_session()
    token_number = issue_next_token(queue_session)
    return Visit.objects.create(
        patient=patient,
        queue_session=queue_session,
        token_number=token_number,
        status=VisitStatus.WAITING,
        priority_level=priority,
        short_note=short_note,
        created_by=created_by,
    )


def waiting_queryset(queue_session: DailyQueueSession | None = None):
    session = queue_session or get_or_create_active_session()
    queryset = Visit.objects.filter(queue_session=session, status=VisitStatus.WAITING)
    app_settings = get_app_settings()
    if app_settings.urgent_cases_jump_queue:
        return queryset.annotate(
            priority_rank=Case(
                When(priority_level=VisitPriority.URGENT, then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            )
        ).order_by("priority_rank", "token_number")
    return queryset.order_by("token_number")


def queue_list_queryset(queue_session: DailyQueueSession | None = None):
    session = queue_session or get_or_create_active_session()
    return (
        Visit.objects.filter(queue_session=session)
        .annotate(
            status_rank=Case(
                When(status=VisitStatus.WITH_DOCTOR, then=Value(0)),
                When(status=VisitStatus.WAITING, then=Value(1)),
                When(status=VisitStatus.SKIPPED, then=Value(2)),
                When(status=VisitStatus.COMPLETED, then=Value(3)),
                default=Value(4),
                output_field=IntegerField(),
            ),
            priority_rank=Case(
                When(priority_level=VisitPriority.URGENT, then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            ),
        )
        .select_related("patient")
        .order_by("status_rank", "priority_rank", "token_number")
    )


@transaction.atomic
def call_next_patient(*, acted_by):
    session = get_or_create_active_session()
    if session.current_visit and session.current_visit.status == VisitStatus.WITH_DOCTOR:
        return session.current_visit

    next_visit = waiting_queryset(session).select_for_update().first()
    if not next_visit:
        session.current_visit = None
        session.save(update_fields=["current_visit", "updated_at"])
        return None

    next_visit.status = VisitStatus.WITH_DOCTOR
    next_visit.called_at = timezone.now()
    next_visit.save(update_fields=["status", "called_at", "updated_at"])

    session.current_visit = next_visit
    session.save(update_fields=["current_visit", "updated_at"])
    return next_visit


@transaction.atomic
def mark_visit_done(visit: Visit, *, acted_by):
    if visit.status != VisitStatus.WITH_DOCTOR:
        raise ValueError("Only with_doctor visits can be marked done.")
    visit.status = VisitStatus.COMPLETED
    visit.completed_at = timezone.now()
    visit.save(update_fields=["status", "completed_at", "updated_at"])
    session = visit.queue_session
    if session.current_visit_id == visit.id:
        session.current_visit = None
        session.save(update_fields=["current_visit", "updated_at"])
    return visit


@transaction.atomic
def skip_visit(visit: Visit, *, acted_by):
    if visit.status not in {VisitStatus.WAITING, VisitStatus.WITH_DOCTOR}:
        raise ValueError("Only waiting or with_doctor visits can be skipped.")
    visit.status = VisitStatus.SKIPPED
    visit.save(update_fields=["status", "updated_at"])
    session = visit.queue_session
    if session.current_visit_id == visit.id:
        session.current_visit = None
        session.save(update_fields=["current_visit", "updated_at"])
    return visit


def cancel_visit(visit: Visit, *, acted_by):
    if visit.status != VisitStatus.WAITING:
        raise ValueError("Only waiting visits can be cancelled.")
    visit.status = VisitStatus.CANCELLED
    visit.save(update_fields=["status", "updated_at"])
    return visit


def requeue_visit(visit: Visit, *, acted_by):
    if visit.status != VisitStatus.SKIPPED:
        raise ValueError("Only skipped visits can be requeued.")
    visit.status = VisitStatus.WAITING
    visit.save(update_fields=["status", "updated_at"])
    return visit


def mark_urgent(visit: Visit, *, acted_by):
    if visit.status not in {VisitStatus.WAITING, VisitStatus.SKIPPED}:
        raise ValueError("Only waiting/skipped visits can be marked urgent.")
    visit.priority_level = VisitPriority.URGENT
    visit.save(update_fields=["priority_level", "updated_at"])
    return visit


@transaction.atomic
def daily_reset(for_date: date | None = None):
    queue_date = for_date or timezone.localdate()
    sessions = DailyQueueSession.objects.select_for_update().filter(queue_date=queue_date, is_active=True)
    sessions.update(is_active=False, current_visit=None, updated_at=timezone.now())
