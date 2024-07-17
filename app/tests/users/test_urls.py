# This work is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
# https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

from django.test import Client, TestCase
from django.urls import reverse


class TestUrls(TestCase):

    def setUp(self):
        self.client = Client()

    def test_logout_url(self):
        url = reverse("logout")
        response = self.client.post(url)
        self.assertEqual(response.status_code, 401)

    def test_signup_url(self):
        url = reverse("signup")
        response = self.client.post(
            url,
            data={
                "email": "test@example.com",
                "password": "testpassword",
                "password_confirm": "testpassword",
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_login_url(self):
        url = reverse("login")
        response = self.client.post(
            url, data={"email": "test@example.com", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 401)

    def test_token_refresh_url(self):
        refresh_token = "valid_refresh_token_here"
        url = reverse("token-refresh")
        response = self.client.post(
            url,
            data={"refresh": refresh_token},
        )
        self.assertEqual(response.status_code, 401)

    def test_profile_url(self):
        url = reverse("user")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_delete_profile_url(self):
        url = reverse("delete-user")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)
