from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from apps.accounts.models import UserRole
from apps.patients.models import GenderChoice, Patient


class AccessControlTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.reception = user_model.objects.create_user(
            username="reception_acl",
            password="testpass123",
            role=UserRole.RECEPTION,
        )
        self.doctor = user_model.objects.create_user(
            username="doctor_acl",
            password="testpass123",
            role=UserRole.DOCTOR,
        )
        self.admin = user_model.objects.create_user(
            username="admin_acl",
            password="testpass123",
            role=UserRole.ADMIN,
            is_staff=True,
        )
        self.client = Client()

    def test_reception_cannot_open_admin_settings(self):
        self.client.force_login(self.reception)
        response = self.client.get(reverse("settings_app:settings-home"))
        self.assertEqual(response.status_code, 403)

    def test_doctor_cannot_open_admin_settings(self):
        self.client.force_login(self.doctor)
        response = self.client.get(reverse("settings_app:settings-home"))
        self.assertEqual(response.status_code, 403)

    def test_public_display_is_read_only_and_public(self):
        response = self.client.get(reverse("display:screen"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "<form", html=False)

    def test_anonymous_user_redirected_from_reception(self):
        response = self.client.get(reverse("reception-dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response["Location"])

    def test_reception_cannot_call_next_action(self):
        self.client.force_login(self.reception)
        response = self.client.post(reverse("queue:call-next"))
        self.assertEqual(response.status_code, 403)

    def test_doctor_cannot_add_existing_patient_to_queue(self):
        patient = Patient.objects.create(
            mr_number="ACL-MR-1",
            full_name="ACL Patient",
            mobile_number="03007778888",
            age=27,
            gender=GenderChoice.MALE,
        )
        self.client.force_login(self.doctor)
        response = self.client.post(
            reverse("queue:add-existing"),
            {"patient_id": patient.id, "priority": "normal", "short_note": ""},
        )
        self.assertEqual(response.status_code, 403)

    def test_pwa_routes_are_exposed(self):
        manifest_response = self.client.get(reverse("pwa-manifest"))
        self.assertIn(manifest_response.status_code, (301, 302))
        sw_response = self.client.get(reverse("pwa-service-worker"))
        self.assertEqual(sw_response.status_code, 200)
        self.assertIn("CACHE_NAME", sw_response.content.decode())
