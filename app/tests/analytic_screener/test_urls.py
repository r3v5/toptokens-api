import pytest
from analytic_screener.models import MarketRecommendation
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
        assert "ticker" in response.data[0]
        assert "price" in response.data[0]
        assert "market_cap" in response.data[0]
        assert "hedge_funds" in response.data[0]


@pytest.mark.django_db
def test_market_indicators_url(api_client, create_user_with_tokens):
    user, access_token = create_user_with_tokens
    url = reverse("market-indicators")
    response = api_client.get(url, HTTP_AUTHORIZATION=f"Bearer {access_token}")

    assert response.status_code == status.HTTP_200_OK

    assert isinstance(response.data, list)
    if response.data:
        assert "id" in response.data[0]
        assert "name" in response.data[0]
        assert "value" in response.data[0]


@pytest.mark.django_db
def test_market_recommendations_url(api_client, create_user_with_tokens):
    user, access_token = create_user_with_tokens
    # Create sample MarketRecommendation instances
    MarketRecommendation.objects.create(type="buy", indicator_name="S&P 500", value=0.5)
    MarketRecommendation.objects.create(
        type="sell", indicator_name="NASDAQ", value=-0.3
    )

    url = reverse("market-recommendations")
    response = api_client.get(url, HTTP_AUTHORIZATION=f"Bearer {access_token}")

    assert response.status_code == status.HTTP_200_OK

    # Verify the structure of the response
    assert "buy_recommendations" in response.data
    assert "sell_recommendations" in response.data
    assert isinstance(response.data["buy_recommendations"], list)
    assert isinstance(response.data["sell_recommendations"], list)

    # Check contents of buy_recommendations
    if response.data["buy_recommendations"]:
        assert "type" in response.data["buy_recommendations"][0]
        assert "indicator_name" in response.data["buy_recommendations"][0]
        assert "value" in response.data["buy_recommendations"][0]
        assert "created_at" in response.data["buy_recommendations"][0]

    # Check contents of sell_recommendations
    if response.data["sell_recommendations"]:
        assert "type" in response.data["sell_recommendations"][0]
        assert "indicator_name" in response.data["sell_recommendations"][0]
        assert "value" in response.data["sell_recommendations"][0]
        assert "created_at" in response.data["sell_recommendations"][0]


@pytest.mark.django_db
def test_hedge_fund_portfolio_url(api_client, create_user_with_tokens):
    user, access_token = create_user_with_tokens
    url = reverse(
        "hedge-fund-portfolios"
    )  # Use reverse to get the URL from the view name
    response = api_client.get(url, HTTP_AUTHORIZATION=f"Bearer {access_token}")

    # Verify that the response status code is 200 OK
    assert response.status_code == status.HTTP_200_OK

    # Verify the content of the response
    assert isinstance(response.data, list)  # Ensure response is a list of hedge funds
    if response.data:
        assert "id" in response.data[0]
        assert "name" in response.data[0]
        assert "cryptocurrencies" in response.data[0]
        assert isinstance(response.data[0]["cryptocurrencies"], list)
