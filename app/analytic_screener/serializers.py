from rest_framework import serializers

from .models import Cryptocurrency, HedgeFund, MarketIndicator


class HedgeFundSerializer(serializers.ModelSerializer):

    class Meta:
        model = HedgeFund
        fields = ["id", "name"]


class CryptocurrencySerializer(serializers.ModelSerializer):
    hedge_funds = HedgeFundSerializer(many=True, read_only=True)

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
            "hedge_funds",
        ]


class MarketIndicatorSerializer(serializers.ModelSerializer):

    class Meta:
        model = MarketIndicator
        fields = ["id", "name", "value"]
