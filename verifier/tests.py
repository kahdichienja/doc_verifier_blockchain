from django.test import TestCase
from django.urls import reverse


class RegistrationViewTests(TestCase):
    def test_invalid_registration_does_not_crash(self):
        response = self.client.post("/registration/", {})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Register")

    def test_successful_registration_redirects_to_login(self):
        response = self.client.post(
            reverse("registration"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))
