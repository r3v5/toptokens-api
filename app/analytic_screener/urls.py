from django.urls import path

from . import views

urlpatterns = [
    path(
        "cryptocurrencies/",
        views.CryptocurrencyAPIView.as_view(),
        name="cryptocurrencies",
    ),
    path(
        "market-indicators/",
        views.MarketIndicatorAPIView.as_view(),
        name="market-indicators",
    ),
    path(
        "market-recommendations/",
        views.MarketRecommendationsAPIView.as_view(),
        name="market-recommendations",
    ),
]
