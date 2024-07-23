import pytest
from analytic_screener.models import Cryptocurrency, HedgeFund
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_get_cryptocurrencies():
    # Setup
    hedge_fund_1 = HedgeFund.objects.create(name="Hedge Fund A")
    hedge_fund_2 = HedgeFund.objects.create(name="Hedge Fund B")

    crypto_1 = Cryptocurrency.objects.create(
        name="Bitcoin",
        ticker="BTC",
        price=50000.00,
        market_cap=1000000000000,
        price_dynamics_for_1_year=10.00,
        price_dynamics_for_6_months=5.00,
        price_dynamics_for_3_months=2.00,
        price_dynamics_for_1_month=1.00,
    )
    crypto_1.hedge_funds.set([hedge_fund_1, hedge_fund_2])

    crypto_2 = Cryptocurrency.objects.create(
        name="Ethereum",
        ticker="ETH",
        price=3000.00,
        market_cap=300000000000,
        price_dynamics_for_1_year=20.00,
        price_dynamics_for_6_months=10.00,
        price_dynamics_for_3_months=4.00,
        price_dynamics_for_1_month=2.00,
    )
    crypto_2.hedge_funds.set([hedge_fund_1])

    client = APIClient()

    # Test
    response = client.get("/api/cryptocurrencies/")
    assert response.status_code == status.HTTP_200_OK
    assert "Bitcoin" in str(response.data)
    assert "Ethereum" in str(response.data)
    assert len(response.data) == 2


@pytest.mark.django_db
def test_get_price_dynamics_1y():
    # Setup
    hedge_fund_1 = HedgeFund.objects.create(name="Hedge Fund A")
    hedge_fund_2 = HedgeFund.objects.create(name="Hedge Fund B")

    crypto_1 = Cryptocurrency.objects.create(
        name="Bitcoin",
        ticker="BTC",
        price=50000.00,
        market_cap=1000000000000,
        price_dynamics_for_1_year=10.00,
    )
    crypto_1.hedge_funds.set([hedge_fund_1, hedge_fund_2])

    crypto_2 = Cryptocurrency.objects.create(
        name="Ethereum",
        ticker="ETH",
        price=3000.00,
        market_cap=300000000000,
        price_dynamics_for_1_year=20.00,
    )
    crypto_2.hedge_funds.set([hedge_fund_1])

    client = APIClient()

    # Test
    response = client.get("/api/price-dynamics-1y/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert (
        response.data[0]["price_dynamics_for_1_year"]
        >= response.data[1]["price_dynamics_for_1_year"]
    )


@pytest.mark.django_db
def test_get_hedge_funds():
    # Setup
    HedgeFund.objects.create(name="Hedge Fund A")
    HedgeFund.objects.create(name="Hedge Fund B")

    client = APIClient()

    # Test
    response = client.get("/api/hedge-funds/")
    assert response.status_code == status.HTTP_200_OK
    assert "Hedge Fund A" in str(response.data)
    assert "Hedge Fund B" in str(response.data)
    assert len(response.data) == 2
