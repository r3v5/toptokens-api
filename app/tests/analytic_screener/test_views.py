import pytest
from analytic_screener.models import Cryptocurrency, HedgeFund, MarketIndicator
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
    # Create sample HedgeFunds
    hedge_fund = HedgeFund.objects.create(name="Top Hedge Fund")

    # Create sample Cryptocurrency and associate with HedgeFund
    cryptocurrency = Cryptocurrency.objects.create(
        name="Bitcoin",
        ticker="BTC",
        price=30000.00,
        market_cap=500000000000,
        price_dynamics_for_1_year=50.00,
        price_dynamics_for_6_months=25.00,
        price_dynamics_for_3_months=10.00,
        price_dynamics_for_1_month=5.00,
    )
    cryptocurrency.hedge_funds.add(hedge_fund)

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
        assert "hedge_funds" in response.data[0]  # Check for nested hedge_funds
        assert isinstance(response.data[0]["hedge_funds"], list)
        if response.data[0]["hedge_funds"]:
            assert "id" in response.data[0]["hedge_funds"][0]
            assert "name" in response.data[0]["hedge_funds"][0]


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
def test_market_indicator_view(api_client, create_user_with_tokens):
    user, access_token = create_user_with_tokens
    # Create sample MarketIndicator instances
    MarketIndicator.objects.create(name="Consumer Confidence Index", value=120)
    MarketIndicator.objects.create(name="Inflation Rate", value=3)

    url = reverse(
        "market-indicators"
    )  # Ensure that this matches the name of your URL pattern
    response = api_client.get(url, HTTP_AUTHORIZATION=f"Bearer {access_token}")

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)
    if response.data:
        assert "id" in response.data[0]
        assert "name" in response.data[0]
        assert "value" in response.data[0]
