import pytest
from analytic_screener.models import (
    Cryptocurrency,
    HedgeFund,
    MarketIndicator,
    MarketRecommendation,
)
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

    # Create sample Cryptocurrencies and associate with HedgeFund
    cryptocurrency_1 = Cryptocurrency.objects.create(
        name="Bitcoin",
        ticker="BTC",
        price=30000.00,
        market_cap=500000000000,
    )
    cryptocurrency_1.hedge_funds.add(hedge_fund)

    cryptocurrency_2 = Cryptocurrency.objects.create(
        name="Ethereum",
        ticker="ETH",
        price=2000.00,
        market_cap=200000000000,
    )
    cryptocurrency_2.hedge_funds.add(hedge_fund)

    url = reverse("cryptocurrencies")

    # Test with descending order
    response = api_client.get(
        url,
        HTTP_AUTHORIZATION=f"Bearer {access_token}",
        data={"order": "desc"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)
    if response.data:
        assert response.data[0]["name"] == "Bitcoin"  # Highest market cap first
        assert "id" in response.data[0]
        assert "name" in response.data[0]
        assert "hedge_funds" in response.data[0]
        assert isinstance(response.data[0]["hedge_funds"], list)
        if response.data[0]["hedge_funds"]:
            assert "id" in response.data[0]["hedge_funds"][0]
            assert "name" in response.data[0]["hedge_funds"][0]

    # Test with ascending order
    response = api_client.get(
        url,
        HTTP_AUTHORIZATION=f"Bearer {access_token}",
        data={"order": "asc"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)
    if response.data:
        assert response.data[0]["name"] == "Ethereum"
        assert "id" in response.data[0]
        assert "name" in response.data[0]
        assert "hedge_funds" in response.data[0]
        assert isinstance(response.data[0]["hedge_funds"], list)
        if response.data[0]["hedge_funds"]:
            assert "id" in response.data[0]["hedge_funds"][0]
            assert "name" in response.data[0]["hedge_funds"][0]


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


@pytest.mark.django_db
def test_market_recommendations_view(api_client, create_user_with_tokens):
    user, access_token = create_user_with_tokens
    # Create sample MarketRecommendation instances
    MarketRecommendation.objects.create(type="buy", indicator_name="S&P 500", value=0.5)
    MarketRecommendation.objects.create(
        type="sell", indicator_name="NASDAQ", value=-0.3
    )

    url = reverse("market-recommendations")
    response = api_client.get(url, HTTP_AUTHORIZATION=f"Bearer {access_token}")

    assert response.status_code == status.HTTP_200_OK
    assert "buy_recommendations" in response.data
    assert "sell_recommendations" in response.data
    assert isinstance(response.data["buy_recommendations"], list)
    assert isinstance(response.data["sell_recommendations"], list)
    if response.data["buy_recommendations"]:
        assert "type" in response.data["buy_recommendations"][0]
        assert "indicator_name" in response.data["buy_recommendations"][0]
        assert "value" in response.data["buy_recommendations"][0]
        assert "created_at" in response.data["buy_recommendations"][0]
    if response.data["sell_recommendations"]:
        assert "type" in response.data["sell_recommendations"][0]
        assert "indicator_name" in response.data["sell_recommendations"][0]
        assert "value" in response.data["sell_recommendations"][0]
        assert "created_at" in response.data["sell_recommendations"][0]
