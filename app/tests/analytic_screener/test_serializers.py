import pytest
from analytic_screener.models import Cryptocurrency, HedgeFund
from analytic_screener.serializers import CryptocurrencySerializer, HedgeFundSerializer


@pytest.mark.django_db
def test_cryptocurrency_serializer():
    # Create a sample Cryptocurrency instance
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


@pytest.mark.django_db
def test_hedge_fund_serializer():
    # Create a sample HedgeFund instance
    hedge_fund = HedgeFund.objects.create(name="Alpha Hedge Fund")

    # Create sample Cryptocurrencies
    crypto1 = Cryptocurrency.objects.create(
        name="Ethereum",
        ticker="ETH",
        price=2000.00,
        market_cap=200000000000,
        price_dynamics_for_1_year=60.00,
        price_dynamics_for_6_months=30.00,
        price_dynamics_for_3_months=15.00,
        price_dynamics_for_1_month=8.00,
    )
    crypto2 = Cryptocurrency.objects.create(
        name="Ripple",
        ticker="XRP",
        price=1.00,
        market_cap=50000000000,
        price_dynamics_for_1_year=10.00,
        price_dynamics_for_6_months=5.00,
        price_dynamics_for_3_months=3.00,
        price_dynamics_for_1_month=1.00,
    )

    # Add cryptocurrencies to hedge fund using the correct related name
    hedge_fund.cryptocurrencies.add(crypto1, crypto2)

    # Serialize the hedge fund instance
    serializer = HedgeFundSerializer(hedge_fund)
    data = serializer.data

    # Assert the serialized data
    assert data["id"] == hedge_fund.id
    assert data["name"] == "Alpha Hedge Fund"
    assert len(data["cryptocurrencies"]) == 2

    # Check that the serialized cryptocurrency data is correct
    crypto_data = data["cryptocurrencies"]
    assert any(c["ticker"] == "ETH" for c in crypto_data)
    assert any(c["ticker"] == "XRP" for c in crypto_data)
