from rest_framework import serializers

from .models import Cryptocurrency, HedgeFund, MarketIndicator


class CryptocurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Cryptocurrency
        fields = [
            "id",
            "name",
            "ticker",
            "price",
            "market_cap",
            "price_dynamics_for_1_year",
            "price_dynamics_for_6_months",
            "price_dynamics_for_3_months",
            "price_dynamics_for_1_month",
        ]


class HedgeFundSerializer(serializers.ModelSerializer):
    cryptocurrencies = CryptocurrencySerializer(many=True, read_only=True)

    class Meta:
        model = HedgeFund
        fields = ["id", "name", "cryptocurrencies"]


class MarketIndicatorSerializer(serializers.ModelSerializer):

    class Meta:
        model = MarketIndicator
        fields = ["id", "name", "value"]
