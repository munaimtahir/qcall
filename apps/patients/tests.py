from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import Client, TestCase
from django.urls import reverse

from apps.accounts.models import UserRole
from apps.patients.models import GenderChoice, Patient


class PatientRegistryTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.reception = user_model.objects.create_user(
            username="reception_test",
            password="testpass123",
            role=UserRole.RECEPTION,
        )
        self.client = Client()
        self.client.force_login(self.reception)

    def test_search_patient_by_mobile_and_mr_number(self):
        patient = Patient.objects.create(
            mr_number="MR1001",
            full_name="Ayesha Khan",
            mobile_number="03001234567",
            age=32,
            gender=GenderChoice.FEMALE,
        )
        response_mobile = self.client.get(reverse("patients:search"), {"q": "0300123"})
        self.assertContains(response_mobile, patient.full_name)

        response_mr = self.client.get(reverse("patients:search"), {"q": "MR1001"})
        self.assertContains(response_mr, patient.full_name)

    def test_prevent_duplicate_mr_number(self):
        Patient.objects.create(
            mr_number="MR999",
            full_name="Patient One",
            mobile_number="03000000001",
            age=20,
            gender=GenderChoice.MALE,
        )
        with self.assertRaises(IntegrityError):
            Patient.objects.create(
                mr_number="MR999",
                full_name="Patient Two",
                mobile_number="03000000002",
                age=22,
                gender=GenderChoice.FEMALE,
            )
