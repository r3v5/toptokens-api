from decimal import Decimal

from django.http import HttpRequest, HttpResponse
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Cryptocurrency, MarketIndicator, MarketRecommendation
from .serializers import (
    CryptocurrencySerializer,
    MarketIndicatorSerializer,
    MarketRecommendationSerializer,
)


class CryptocurrencyAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest) -> HttpRequest:
        order = request.query_params.get("order", "desc")

        if order not in ["asc", "desc"]:
            return Response(
                {"error": "Invalid order specified"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Retrieve all cryptocurrencies
            cryptocurrencies = Cryptocurrency.objects.all().prefetch_related(
                "hedge_funds"
            )

            # Serialize the data
            serializer = CryptocurrencySerializer(cryptocurrencies, many=True)
            data = serializer.data

            # Sort by market cap
            try:
                result = sorted(
                    data,
                    key=lambda x: Decimal(x.get("market_cap", 0)),
                    reverse=(
                        order == "desc"
                    ),  # `reverse=True` for descending, `reverse=False` for ascending
                )
            except (ValueError, TypeError):
                return Response(
                    {"error": "Invalid data format for sorting"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MarketRecommendationsAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest) -> HttpResponse:
        buy_recommendations = MarketRecommendation.objects.filter(type="buy")
        sell_recommendations = MarketRecommendation.objects.filter(type="sell")

        buy_serializer = MarketRecommendationSerializer(buy_recommendations, many=True)
        sell_serializer = MarketRecommendationSerializer(
            sell_recommendations, many=True
        )

        return Response(
            {
                "buy_recommendations": buy_serializer.data,
                "sell_recommendations": sell_serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class MarketIndicatorAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest) -> HttpResponse:
        try:
            market_indicators = MarketIndicator.objects.all()
            serializer = MarketIndicatorSerializer(market_indicators, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
