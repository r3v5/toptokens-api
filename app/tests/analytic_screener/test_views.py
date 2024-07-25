import pytest
from analytic_screener.models import Cryptocurrency, HedgeFund
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
    access_token = str(RefreshToken.for_user(user).access_token)
    return user, access_token


@pytest.mark.django_db
def test_cryptocurrency_view_with_valid_params(api_client, create_user_with_tokens):
    user, access_token = create_user_with_tokens
    # Create sample data
    Cryptocurrency.objects.create(
        name="Bitcoin",
        ticker="BTC",
        price="30000.00",
        market_cap="500000000000",
        price_dynamics_for_1_year="50.0",
        price_dynamics_for_6_months="10.0",
        price_dynamics_for_3_months="5.0",
        price_dynamics_for_1_month="1.0",
    )
    url = reverse("cryptocurrencies")
    response = api_client.get(
        url,
        HTTP_AUTHORIZATION=f"Bearer {access_token}",
        data={"period": "1_year", "order": "desc"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)
    if response.data:
        assert "id" in response.data[0]
        assert "name" in response.data[0]
        assert "price_dynamics_for_1_year" in response.data[0]


@pytest.mark.django_db
def test_cryptocurrency_view_with_invalid_order(api_client, create_user_with_tokens):
    user, access_token = create_user_with_tokens
    url = reverse("cryptocurrencies")
    response = api_client.get(
        url, HTTP_AUTHORIZATION=f"Bearer {access_token}", data={"order": "invalid"}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"] == "Invalid order specified"


@pytest.mark.django_db
def test_hedge_funds_view(api_client, create_user_with_tokens):
    user, access_token = create_user_with_tokens
    # Create sample data
    hedge_fund = HedgeFund.objects.create(name="Top Hedge Fund")
    cryptocurrency = Cryptocurrency.objects.create(
        name="Bitcoin",
        ticker="BTC",
        price=30000.00,
        market_cap=500000000000,
        price_dynamics_for_1_year=50.00,
        price_dynamics_for_6_months=10.00,
        price_dynamics_for_3_months=5.00,
        price_dynamics_for_1_month=1.00,
    )
    cryptocurrency.hedge_funds.add(hedge_fund)  # Use the ManyToManyField's add method
    url = reverse("hedge-funds")
    response = api_client.get(url, HTTP_AUTHORIZATION=f"Bearer {access_token}")

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)
    if response.data:
        assert "id" in response.data[0]
        assert "name" in response.data[0]
        assert "cryptocurrencies" in response.data[0]
        assert isinstance(response.data[0]["cryptocurrencies"], list)
