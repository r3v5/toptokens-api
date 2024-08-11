import pytest
from analytic_screener.models import (
    Cryptocurrency,
    HedgeFund,
    MarketIndicator,
    MarketRecommendation,
)
from analytic_screener.serializers import (
    CryptocurrencySerializer,
    HedgeFundSerializer,
    MarketIndicatorSerializer,
    MarketRecommendationSerializer,
)
from django.utils import timezone


@pytest.mark.django_db
def test_cryptocurrency_serializer():
    # Create sample HedgeFunds
    hedge_fund1 = HedgeFund.objects.create(name="Hedge Fund A")
    hedge_fund2 = HedgeFund.objects.create(name="Hedge Fund B")

    # Create a sample Cryptocurrency instance and associate it with hedge funds
    cryptocurrency = Cryptocurrency.objects.create(
        name="Bitcoin",
        ticker="BTC",
        price=30000.00,
        market_cap=500000000000,
    )
    cryptocurrency.hedge_funds.add(hedge_fund1, hedge_fund2)

    # Serialize the instance
    serializer = CryptocurrencySerializer(cryptocurrency)
    data = serializer.data

    # Assert that the serialized data matches the expected output
    assert data["id"] == cryptocurrency.id
    assert data["name"] == "Bitcoin"
    assert data["ticker"] == "BTC"
    assert data["price"] == 30000.00
    assert data["market_cap"] == 500000000000

    # Check the nested hedge_funds data
    hedge_funds_data = data["hedge_funds"]
    assert len(hedge_funds_data) == 2
    assert any(hf["name"] == "Hedge Fund A" for hf in hedge_funds_data)
    assert any(hf["name"] == "Hedge Fund B" for hf in hedge_funds_data)


@pytest.mark.django_db
def test_hedge_fund_serializer():
    # Create a sample HedgeFund instance
    hedge_fund = HedgeFund.objects.create(name="Alpha Hedge Fund")

    # Serialize the hedge fund instance
    serializer = HedgeFundSerializer(hedge_fund)
    data = serializer.data

    # Assert that the serialized data matches the expected output
    assert data["id"] == hedge_fund.id
    assert data["name"] == "Alpha Hedge Fund"


@pytest.mark.django_db
def test_market_indicator_serializer():
    # Create a sample MarketIndicator instance
    market_indicator = MarketIndicator.objects.create(
        name="SPX Fear & Greed Index", value=35
    )

    # Serialize the instance
    serializer = MarketIndicatorSerializer(market_indicator)
    data = serializer.data

    # Assert that the serialized data matches the expected output
    assert data["id"] == market_indicator.id
    assert data["name"] == market_indicator.name
    assert data["value"] == market_indicator.value


@pytest.mark.django_db
def test_market_recommendation_serializer():
    # Create a sample MarketRecommendation instance with the current time
    market_recommendation = MarketRecommendation.objects.create(
        type="buy", index_name="Crypto Market", value=30
    )

    # Serialize the instance
    serializer = MarketRecommendationSerializer(market_recommendation)
    data = serializer.data

    # Assert that the serialized data matches the expected output
    assert data["type"] == "buy"
    assert data["index_name"] == "Crypto Market"
    assert data["value"] == 30

    # Check the created_at field format
    created_at = data["created_at"]
    assert created_at is not None

    # Convert created_at to the same time zone as your serializer output
    local_created_at = market_recommendation.created_at.astimezone(
        timezone.get_current_timezone()
    )
    expected_created_at = local_created_at.strftime("%B %d, %Y, %I:%M %p")

    # Adjust the assertion to check against the expected formatted time
    assert created_at == expected_created_at
