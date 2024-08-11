from rest_framework import serializers

from .models import Cryptocurrency, HedgeFund, MarketIndicator, MarketRecommendation


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
            "hedge_funds",
        ]


class MarketIndicatorSerializer(serializers.ModelSerializer):

    class Meta:
        model = MarketIndicator
        fields = ["id", "name", "value"]


class MarketRecommendationSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%B %d, %Y, %I:%M %p")

    class Meta:
        model = MarketRecommendation
        fields = ("type", "index_name", "value", "created_at")
