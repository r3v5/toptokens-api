from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import OutstandingToken
from users.views import generate_tokens_for_user

User = get_user_model()


class TestUrls(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com", password="testpassword"
        )
        tokens = generate_tokens_for_user(self.user)
        self.access_token = tokens["access_token"]
        self.refresh_token = tokens["refresh_token"]

        # Set the access token in the request header for authenticated requests
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_logout_url(self):
        url = reverse("logout")
        data = {"refresh_token": self.refresh_token}
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_signup_url(self):
        url = reverse("signup")
        response = self.client.post(
            url,
            data={
                "email": "new@example.com",
                "password": "newpassword",
                "password_confirm": "newpassword",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_url(self):
        url = reverse("login")
        response = self.client.post(
            url,
            data={"email": "test@example.com", "password": "testpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)

    def test_token_refresh_url(self):
        url = reverse("token-refresh")
        response = self.client.post(
            url, data={"refresh": self.refresh_token}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_url(self):
        url = reverse("profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_profile_url(self):
        url = reverse("delete-user")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(email="test@example.com").exists())
