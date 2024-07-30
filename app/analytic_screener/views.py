from decimal import Decimal

from django.http import HttpRequest, HttpResponse
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Cryptocurrency, MarketIndicator
from .serializers import CryptocurrencySerializer, MarketIndicatorSerializer


class CryptocurrencyAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest) -> HttpRequest:
        """
        Filter cryptocurrencies based on price dynamics for a specified period and sort by price percentage change or market cap.
        Accepts query parameters:
        - period: '1_year', '6_months', '3_months', '1_month' (optional)
        - order: 'asc' or 'desc' (optional, default is 'desc')
        """
        period = request.query_params.get("period")
        order = request.query_params.get("order", "desc")

        if order not in ["asc", "desc"]:
            return Response(
                {"error": "Invalid order specified"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            if period:
                # Determine which field to use based on the period query parameter
                if period == "1_year":
                    price_dynamics_field = "price_dynamics_for_1_year"
                elif period == "6_months":
                    price_dynamics_field = "price_dynamics_for_6_months"
                elif period == "3_months":
                    price_dynamics_field = "price_dynamics_for_3_months"
                elif period == "1_month":
                    price_dynamics_field = "price_dynamics_for_1_month"
                else:
                    return Response(
                        {"error": "Invalid period specified"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Filter cryptocurrencies with non-null price dynamics for the chosen period
                cryptocurrencies = Cryptocurrency.objects.filter(
                    **{f"{price_dynamics_field}__isnull": False}
                ).prefetch_related("hedge_funds")

                # Serialize the data
                serializer = CryptocurrencySerializer(cryptocurrencies, many=True)
                data = serializer.data

                # Sort by price dynamics field
                try:
                    result = sorted(
                        data,
                        key=lambda x: Decimal(x.get(price_dynamics_field, 0)),
                        reverse=(
                            order == "desc"
                        ),  # `reverse=True` for descending, `reverse=False` for ascending
                    )
                except (ValueError, TypeError):
                    return Response(
                        {"error": "Invalid data format for sorting"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            else:
                # No period specified, sort by market cap by default
                cryptocurrencies = Cryptocurrency.objects.all().prefetch_related(
                    "hedge_funds"
                )

                # Serialize the data
                serializer = CryptocurrencySerializer(cryptocurrencies, many=True)
                data = serializer.data

                # Sort by market cap
                result = sorted(
                    data,
                    key=lambda x: Decimal(x.get("market_cap", 0)),
                    reverse=(
                        order == "desc"
                    ),  # `reverse=True` for descending, `reverse=False` for ascending
                )

            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
