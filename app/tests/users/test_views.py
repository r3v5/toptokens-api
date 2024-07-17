# This work is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
# https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user_with_tokens():
    user = CustomUser.objects.create_user(
        email="test@example.com", password="strongpassword"
    )
    refresh_token = str(RefreshToken.for_user(user).access_token)
    return user, refresh_token


@pytest.mark.django_db
def test_signup_api_view(api_client):
    url = reverse("signup")
    data = {
        "email": "test@example.com",
        "password": "strongpassword",
        "password_confirm": "strongpassword",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert CustomUser.objects.filter(email=data["email"]).exists()


@pytest.mark.django_db
def test_signup_api_view_passwords_not_matching(api_client):
    url = reverse("signup")
    data = {
        "email": "test@example.com",
        "password": "strongpassword",
        "password_confirm": "differentpassword",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_login_api_view(api_client):
    CustomUser.objects.create_user(email="test@example.com", password="strongpassword")
    url = reverse("login")
    data = {"email": "test@example.com", "password": "strongpassword"}
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.data
    assert "refresh_token" in response.data


@pytest.mark.django_db
def test_login_api_view_invalid_credentials(api_client):
    url = reverse("login")
    data = {"email": "nonexistent@example.com", "password": "password"}
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_user_api_view(api_client, create_user_with_tokens):
    user, access_token = create_user_with_tokens
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    url = reverse("user")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == user.id


@pytest.mark.django_db
def test_delete_user_api_view(api_client, create_user_with_tokens):
    user, access_token = create_user_with_tokens
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    url = reverse("delete-user")
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not CustomUser.objects.filter(id=user.id).exists()


User = get_user_model()


class TestLogoutAPIView(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com", password="password"
        )
        self.refresh_token = str(RefreshToken().for_user(self.user))

    def test_logout_success(self):
        self.client.force_authenticate(user=self.user)
        data = {"refresh_token": self.refresh_token}
        response = self.client.post("/api/v1/users/logout/", data=data)

        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertEqual(response.data["message"], "Logout successfully")

        # Check if the user is inactive after logout
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_logout_missing_refresh_token(self):
        self.client.force_authenticate(user=self.user)
        data = {}  # Missing refresh_token
        response = self.client.post("/api/v1/users/logout/", data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_unauthenticated(self):
        response = self.client.post("/api/v1/users/logout/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
