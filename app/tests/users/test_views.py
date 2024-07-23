from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import OutstandingToken, RefreshToken
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
    formatted_date_joined = user.date_joined.strftime("%Y-%m-%d")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == user.email
    assert response.data["date_joined"] == formatted_date_joined


@pytest.mark.django_db
def test_delete_user_api_view(api_client, create_user_with_tokens):
    user, access_token = create_user_with_tokens
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    url = reverse("delete-user")
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not CustomUser.objects.filter(id=user.id).exists()


@pytest.mark.django_db
def test_logout_api_view(api_client, create_user_with_tokens):
    user, access_token = create_user_with_tokens
    refresh_token = str(
        RefreshToken.for_user(user)
    )  # Generate a new refresh token if necessary
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    url = reverse("logout")
    data = {"refresh_token": refresh_token}
    response = api_client.post(url, data=data, format="json")

    assert response.status_code == status.HTTP_205_RESET_CONTENT
    assert response.data["message"] == "Logout successfully"

    # Check if the user is inactive after logout
    user.refresh_from_db()
    assert not user.is_active


@pytest.mark.django_db
def test_logout_missing_refresh_token(api_client, create_user_with_tokens):
    user, access_token = create_user_with_tokens
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    url = reverse("logout")
    data = {}  # Missing refresh_token
    response = api_client.post(url, data=data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_logout_unauthenticated(api_client):
    url = reverse("logout")
    response = api_client.post(url, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_delete_refresh_tokens(api_client: APIClient):
    # Create a test user
    user = CustomUser.objects.create_user(
        email="test@example.com", password="password123"
    )

    # Create an OutstandingToken with all required fields
    OutstandingToken.objects.create(
        user=user,
        jti="some-jti",
        token="some-token",
        created_at=timezone.now(),
        expires_at=timezone.now()
        + timedelta(days=1),  # Provide a valid expiration time
    )

    # Delete the user
    CustomUser.objects.filter(id=user.id).delete()

    # Verify the token exists with `user=None`
    assert OutstandingToken.objects.filter(user=None).exists()

    # Send a DELETE request to the endpoint
    response = api_client.delete("/api/v1/users/token/delete-tokens-with-none-users/")

    # Verify the response status and message
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data["message"] == "Tokens associated with Null users are deleted"

    # Verify the token has been deleted
    assert not OutstandingToken.objects.filter(user=None).exists()
