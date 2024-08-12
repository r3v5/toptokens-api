import os
from typing import Dict

import requests
from analytic_screener.models import (
    Cryptocurrency,
    HedgeFund,
    MarketIndicator,
    MarketRecommendation,
)
from bs4 import BeautifulSoup
from celery import shared_task


@shared_task
def parse_tier_1_portfolios():
    urls = {
        "Andreessen Horowitz": "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category=andreessen-horowitz-a16z-portfolio",
        "Paradigm": "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category=paradigm-portfolio",
        "Galaxy Digital": "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category=galaxy-digital-portfolio",
        "Sequoia Capital Portfolio": "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category=sequoia-capital-portfolio",
        "Animoca Brands": "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category=animoca-brands",
        "Pantera Capital": "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category=pantera-capital-portfolio",
        "DragonFly Capital": "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category=dragonfly-capital-portfolio",
        "Multicoin Capital": "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category=multicoin-capital-portfolio",
        "Coinbase Ventures": "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category=coinbase-ventures-portfolio",
        "Blockchain Capital": "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category=blockchain-capital-portfolio",
        "Delphi Digital": "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category=delphi-digital-portfolio",
    }
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": os.environ.get("COINGECKO_API_KEY"),
    }

    for hedge_fund_name, url in urls.items():
        response = requests.get(url, headers=headers)
        tokens = response.json()

        # Initialize the dictionary
        token_dict = {}

        # Filter tokens and populate the dictionary
        for token in tokens:
            market_cap = token.get("market_cap")
            if market_cap is not None and market_cap > 100000000:
                ticker = token["symbol"].upper()
                if ticker not in token_dict:
                    token_dict[ticker] = {
                        "name": token["name"],
                        "current_price": token["current_price"],
                        "market_cap": market_cap,
                    }

        # Update or create cryptocurrencies
        for ticker, data in token_dict.items():
            cryptocurrency, created = Cryptocurrency.objects.update_or_create(
                ticker=ticker,
                defaults={
                    "name": data["name"],
                    "price": data["current_price"],
                    "market_cap": data["market_cap"],
                },
            )

            # Get or create the hedge fund and add the cryptocurrency
            hedge_fund, created = HedgeFund.objects.get_or_create(name=hedge_fund_name)
            if not created:
                hedge_fund.cryptocurrencies.add(cryptocurrency)

        print(f"Processed hedge fund portfolio: {hedge_fund_name}")


class FearAndGreedIndex:
    def __init__(self, url: str, headers: Dict = None) -> None:
        self.url = url
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        }

    def get_stock_market_index(self) -> int:
        if self.url != "https://feargreedmeter.com/":
            return -1

        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            div_element = soup.find(
                "div", class_="text-center text-4xl font-semibold mb-1 text-white"
            )
            if div_element:
                return int(div_element.text.strip())
        return -1

    def get_crypto_index(self) -> int:
        if self.url != "https://api.alternative.me/fng/":
            return -1

        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return int(data["data"][0]["value"])
        return -1


@shared_task
def update_fear_and_greed_indices():
    # Initialize Fear and Greed Index instances
    stock_market_index = FearAndGreedIndex(url="https://feargreedmeter.com/")
    crypto_market_index = FearAndGreedIndex(url="https://api.alternative.me/fng/")

    # Fetch the indices
    stock_index = stock_market_index.get_stock_market_index()
    crypto_index = crypto_market_index.get_crypto_index()

    # Clear existing recommendations
    MarketRecommendation.objects.all().delete()

    # Update or create MarketIndicators
    if stock_index != -1:
        MarketIndicator.objects.update_or_create(
            name="Fear & Greed Stock Market Index", defaults={"value": stock_index}
        )
        # Check the stock market index
        if stock_index < 45:
            MarketRecommendation.objects.create(
                type="buy", index_name="Fear & Greed Stock Market", value=stock_index
            )
        elif stock_index > 55:
            MarketRecommendation.objects.create(
                type="sell", index_name="Fear & Greed Stock Market", value=stock_index
            )

    if crypto_index != -1:
        MarketIndicator.objects.update_or_create(
            name="Fear & Greed Crypto Market Index", defaults={"value": crypto_index}
        )
        # Check the crypto market index
        if crypto_index < 45:
            MarketRecommendation.objects.create(
                type="buy", index_name="Fear & Greed Crypto Market", value=crypto_index
            )
        elif crypto_index > 55:
            MarketRecommendation.objects.create(
                type="sell", index_name="Fear & Greed Crypto Market", value=crypto_index
            )

    return {
        "status": "Recommendations and indicators updated",
        "buy_list": list(MarketRecommendation.objects.filter(type="buy").values()),
        "sell_list": list(MarketRecommendation.objects.filter(type="sell").values()),
        "indicators": list(MarketIndicator.objects.all().values()),
    }
