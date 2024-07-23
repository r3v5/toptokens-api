from django.urls import path

from . import views

urlpatterns = [
    path(
        "cryptocurrencies/",
        views.CryptocurrencyAPIView.as_view(),
        name="cryptocurrencies",
    ),
    path(
        "cryptocurrencies/price-dynamics-for-1y/",
        views.PriceDynamics1YAPIView.as_view(),
        name="price-dynamics-for-1y",
    ),
    path("hedge-funds/", views.HedgeFundsAPIView.as_view(), name="hedge-funds"),
]
