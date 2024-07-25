import pytest
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
def test_cryptocurrency_url(api_client, create_user_with_tokens):
    user, access_token = create_user_with_tokens
    url = reverse("cryptocurrencies")  # Use reverse to get the URL from the view name
    response = api_client.get(url, HTTP_AUTHORIZATION=f"Bearer {access_token}")

    # Verify that the response status code is 200 OK
    assert response.status_code == status.HTTP_200_OK

    # Verify the content of the response
    assert isinstance(
        response.data, list
    )  # Ensure response is a list of cryptocurrencies
    if response.data:
        assert "id" in response.data[0]
        assert "name" in response.data[0]
        assert "price" in response.data[0]


@pytest.mark.django_db
def test_hedge_funds_url(api_client, create_user_with_tokens):
    user, access_token = create_user_with_tokens
    url = reverse("hedge-funds")  # Use reverse to get the URL from the view name
    response = api_client.get(url, HTTP_AUTHORIZATION=f"Bearer {access_token}")

    # Verify that the response status code is 200 OK
    assert response.status_code == status.HTTP_200_OK

    # Verify the content of the response
    assert isinstance(response.data, list)  # Ensure response is a list of hedge funds
    if response.data:
        assert "id" in response.data[0]
        assert "name" in response.data[0]
        assert "cryptocurrencies" in response.data[0]
