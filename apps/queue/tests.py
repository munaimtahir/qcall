from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import Client, TestCase
from django.urls import reverse

from apps.accounts.models import UserRole
from apps.patients.models import GenderChoice, Patient
from apps.queue.services import (
    daily_reset,
    call_next_patient,
    enqueue_patient,
    get_or_create_active_session,
    requeue_visit,
    skip_visit,
)
from apps.settings_app.services import get_app_settings
from apps.visits.models import Visit, VisitPriority, VisitStatus


class QueueServiceTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.reception = user_model.objects.create_user(
            username="reception_queue",
            password="testpass123",
            role=UserRole.RECEPTION,
        )
        self.doctor = user_model.objects.create_user(
            username="doctor_queue",
            password="testpass123",
            role=UserRole.DOCTOR,
        )

    def _patient(self, suffix: str):
        return Patient.objects.create(
            mr_number=f"MR{suffix}",
            full_name=f"Patient {suffix}",
            mobile_number=f"0300000{suffix}",
            age=30,
            gender=GenderChoice.MALE,
        )

    def test_create_active_daily_queue_session(self):
        session_1 = get_or_create_active_session()
        session_2 = get_or_create_active_session()
        self.assertEqual(session_1.id, session_2.id)

    def test_issue_sequential_token_numbers(self):
        visit_1 = enqueue_patient(patient=self._patient("1"), created_by=self.reception)
        visit_2 = enqueue_patient(patient=self._patient("2"), created_by=self.reception)
        self.assertEqual(visit_1.token_number, 1)
        self.assertEqual(visit_2.token_number, 2)

    def test_ensure_only_one_with_doctor_visit_per_session(self):
        session = get_or_create_active_session()
        Visit.objects.create(
            patient=self._patient("3"),
            queue_session=session,
            token_number=1,
            status=VisitStatus.WITH_DOCTOR,
            priority_level=VisitPriority.NORMAL,
            created_by=self.reception,
        )
        with self.assertRaises(IntegrityError):
            Visit.objects.create(
                patient=self._patient("4"),
                queue_session=session,
                token_number=2,
                status=VisitStatus.WITH_DOCTOR,
                priority_level=VisitPriority.NORMAL,
                created_by=self.reception,
            )

    def test_urgent_patient_ordering_when_setting_enabled(self):
        settings_obj = get_app_settings()
        settings_obj.urgent_cases_jump_queue = True
        settings_obj.save(update_fields=["urgent_cases_jump_queue"])

        enqueue_patient(patient=self._patient("5"), created_by=self.reception, priority=VisitPriority.NORMAL)
        urgent_visit = enqueue_patient(patient=self._patient("6"), created_by=self.reception, priority=VisitPriority.URGENT)
        called = call_next_patient(acted_by=self.doctor)
        self.assertEqual(called.id, urgent_visit.id)

    def test_skipped_patient_can_be_requeued(self):
        visit = enqueue_patient(patient=self._patient("7"), created_by=self.reception)
        skip_visit(visit, acted_by=self.doctor)
        self.assertEqual(visit.status, VisitStatus.SKIPPED)
        requeue_visit(visit, acted_by=self.reception)
        visit.refresh_from_db()
        self.assertEqual(visit.status, VisitStatus.WAITING)


class QueueWorkflowTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.reception = user_model.objects.create_user(
            username="reception_flow",
            password="testpass123",
            role=UserRole.RECEPTION,
        )
        self.doctor = user_model.objects.create_user(
            username="doctor_flow",
            password="testpass123",
            role=UserRole.DOCTOR,
        )
        self.patient = Patient.objects.create(
            mr_number="MRFLOW",
            full_name="Flow Patient",
            mobile_number="03111111111",
            age=28,
            gender=GenderChoice.FEMALE,
        )
        self.client = Client()

    def test_reception_adds_existing_patient_to_queue(self):
        self.client.force_login(self.reception)
        response = self.client.post(
            reverse("queue:add-existing"),
            {"patient_id": self.patient.id, "priority": VisitPriority.NORMAL, "short_note": "Returning"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Visit.objects.count(), 1)
        self.assertEqual(Visit.objects.first().patient_id, self.patient.id)

    def test_doctor_call_next_then_mark_done(self):
        visit = enqueue_patient(patient=self.patient, created_by=self.reception)
        self.client.force_login(self.doctor)
        call_response = self.client.post(reverse("queue:call-next"))
        self.assertEqual(call_response.status_code, 200)
        visit.refresh_from_db()
        self.assertEqual(visit.status, VisitStatus.WITH_DOCTOR)

        done_response = self.client.post(reverse("queue:done", args=[visit.id]))
        self.assertEqual(done_response.status_code, 200)
        visit.refresh_from_db()
        self.assertEqual(visit.status, VisitStatus.COMPLETED)

    def test_token_unique_within_session(self):
        session = get_or_create_active_session()
        Visit.objects.create(
            patient=self.patient,
            queue_session=session,
            token_number=99,
            status=VisitStatus.WAITING,
            priority_level=VisitPriority.NORMAL,
            created_by=self.reception,
        )
        with self.assertRaises(IntegrityError):
            Visit.objects.create(
                patient=Patient.objects.create(
                    full_name="Another Patient",
                    mobile_number="03222222222",
                    age=40,
                    gender=GenderChoice.MALE,
                ),
                queue_session=session,
                token_number=99,
                status=VisitStatus.WAITING,
                priority_level=VisitPriority.NORMAL,
                created_by=self.reception,
            )

    def test_reception_can_cancel_waiting_visit(self):
        visit = enqueue_patient(patient=self.patient, created_by=self.reception)
        self.client.force_login(self.reception)
        response = self.client.post(reverse("queue:cancel", args=[visit.id]))
        self.assertEqual(response.status_code, 200)
        visit.refresh_from_db()
        self.assertEqual(visit.status, VisitStatus.CANCELLED)

    def test_daily_reset_archives_session_and_restarts_token(self):
        first_visit = enqueue_patient(patient=self.patient, created_by=self.reception)
        old_session = first_visit.queue_session
        daily_reset()
        old_session.refresh_from_db()
        self.assertFalse(old_session.is_active)

        next_patient = Patient.objects.create(
            full_name="Reset Patient",
            mobile_number="03333333333",
            age=31,
            gender=GenderChoice.FEMALE,
        )
        second_visit = enqueue_patient(patient=next_patient, created_by=self.reception)
        self.assertNotEqual(second_visit.queue_session_id, old_session.id)
        self.assertEqual(second_visit.token_number, 1)
