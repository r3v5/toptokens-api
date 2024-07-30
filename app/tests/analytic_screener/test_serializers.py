import pytest
from analytic_screener.models import Cryptocurrency, HedgeFund, MarketIndicator
from analytic_screener.serializers import (
    CryptocurrencySerializer,
    HedgeFundSerializer,
    MarketIndicatorSerializer,
)


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
        price_dynamics_for_1_year=50.00,
        price_dynamics_for_6_months=25.00,
        price_dynamics_for_3_months=10.00,
        price_dynamics_for_1_month=5.00,
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
    assert data["price_dynamics_for_1_year"] == "50.00"
    assert data["price_dynamics_for_6_months"] == "25.00"
    assert data["price_dynamics_for_3_months"] == "10.00"
    assert data["price_dynamics_for_1_month"] == "5.00"

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
