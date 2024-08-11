import pytest
from analytic_screener.models import (
    Cryptocurrency,
    HedgeFund,
    MarketIndicator,
    MarketRecommendation,
)
from django.db.utils import IntegrityError


@pytest.mark.django_db
def test_hedge_fund_creation():
    # Create a HedgeFund instance
    hedge_fund = HedgeFund.objects.create(name="Example Hedge Fund")

    # Retrieve the HedgeFund instance from the database
    retrieved_hedge_fund = HedgeFund.objects.get(id=hedge_fund.id)

    # Check if the hedge fund was created and retrieved correctly
    assert retrieved_hedge_fund.name == "Example Hedge Fund"


@pytest.mark.django_db
def test_cryptocurrency_creation():
    # Create a HedgeFund instance
    hedge_fund = HedgeFund.objects.create(name="Example Hedge Fund")

    # Create a Cryptocurrency instance
    cryptocurrency = Cryptocurrency.objects.create(
        name="Bitcoin",
        ticker="BTC",
        price=30000.00,
        market_cap=600000000000,
    )
    cryptocurrency.hedge_funds.add(hedge_fund)

    # Retrieve the Cryptocurrency instance from the database
    retrieved_cryptocurrency = Cryptocurrency.objects.get(id=cryptocurrency.id)

    # Check if the cryptocurrency was created and retrieved correctly
    assert retrieved_cryptocurrency.name == "Bitcoin"
    assert retrieved_cryptocurrency.ticker == "BTC"
    assert retrieved_cryptocurrency.price == 30000.00
    assert retrieved_cryptocurrency.market_cap == 600000000000

    # Check the related HedgeFunds
    assert retrieved_cryptocurrency.hedge_funds.count() == 1
    assert retrieved_cryptocurrency.hedge_funds.first().name == "Example Hedge Fund"


@pytest.mark.django_db
def test_cryptocurrency_without_required_fields():
    # Try to create a Cryptocurrency without required fields
    with pytest.raises(IntegrityError):
        Cryptocurrency.objects.create(
            name="Incomplete Crypto",
            ticker="INC",
            price=None,
            market_cap=None,
        )


@pytest.mark.django_db
def test_market_indicator_model():
    crypto_fear_and_greed_index = MarketIndicator.objects.create(
        name="Crypto Fear & Greed Index", value=71
    )
    retrieved_crypto_fear_and_greed_index = MarketIndicator.objects.get(
        id=crypto_fear_and_greed_index.id
    )
    assert retrieved_crypto_fear_and_greed_index.name == "Crypto Fear & Greed Index"
    assert retrieved_crypto_fear_and_greed_index.value == 71


@pytest.mark.django_db
def test_market_recommendation_creation():
    # Create a MarketRecommendation instance
    market_recommendation = MarketRecommendation.objects.create(
        type="buy", index_name="Crypto Market", value=30
    )

    # Retrieve the MarketRecommendation instance from the database
    retrieved_market_recommendation = MarketRecommendation.objects.get(
        id=market_recommendation.id
    )

    # Check if the MarketRecommendation was created and retrieved correctly
    assert retrieved_market_recommendation.type == "buy"
    assert retrieved_market_recommendation.index_name == "Crypto Market"
    assert retrieved_market_recommendation.value == 30
    assert retrieved_market_recommendation.created_at is not None
