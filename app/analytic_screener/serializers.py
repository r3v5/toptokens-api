from typing import Any, Dict, List

from rest_framework import serializers

from .models import Cryptocurrency, HedgeFund, MarketIndicator, MarketRecommendation


class HedgeFundSerializer(serializers.ModelSerializer):
    class Meta:
        model = HedgeFund
        fields = ["id", "name"]


class CryptocurrencySerializer(serializers.ModelSerializer):
    hedge_funds = serializers.SerializerMethodField()

    class Meta:
        model = Cryptocurrency
        fields: List[str] = [
            "id",
            "name",
            "ticker",
            "price",
            "market_cap",
            "hedge_funds",
        ]

    def get_hedge_funds(self, obj: Cryptocurrency) -> List[Dict[str, Any]]:
        # Serialize only basic fields to avoid recursion
        return HedgeFundSerializer(obj.hedge_funds.all(), many=True).data


class HedgeFundDetailSerializer(serializers.ModelSerializer):
    cryptocurrencies = serializers.SerializerMethodField()

    class Meta:
        model = HedgeFund
        fields: List[str] = ["id", "name", "cryptocurrencies"]

    def get_cryptocurrencies(self, obj: HedgeFund) -> List[Dict[str, Any]]:
        # Serialize only basic fields to avoid recursion
        return CryptocurrencySerializer(obj.cryptocurrencies.all(), many=True).data


class MarketIndicatorSerializer(serializers.ModelSerializer):

    class Meta:
        model = MarketIndicator
        fields = ["id", "name", "value"]


class MarketRecommendationSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%B %d, %Y, %I:%M %p")

    class Meta:
        model = MarketRecommendation
        fields = ("type", "indicator_name", "value", "created_at")
