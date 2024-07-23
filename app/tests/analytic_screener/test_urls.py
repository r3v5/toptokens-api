import pytest
from analytic_screener.models import Cryptocurrency, HedgeFund
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class TestUrls(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Create a test user
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )

        # Generate tokens for the user
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.refresh_token = str(refresh)

        # Set the access token in the request header for authenticated requests
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        # Set up test data for HedgeFunds
        self.hedge_fund1 = HedgeFund.objects.create(name="Hedge Fund A")
        self.hedge_fund2 = HedgeFund.objects.create(name="Hedge Fund B")

        # Set up test data for Cryptocurrencies
        self.cryptocurrency = Cryptocurrency.objects.create(
            name="Bitcoin",
            ticker="BTC",
            price=30000.00,
            market_cap=500000000000,
            price_dynamics_for_1_year=0.30,
            price_dynamics_for_6_months=0.15,
            price_dynamics_for_3_months=0.05,
            price_dynamics_for_1_month=0.02,
        )
        self.cryptocurrency.hedge_funds.add(self.hedge_fund1, self.hedge_fund2)

    def test_cryptocurrencies_url(self):
        url = reverse("cryptocurrencies")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Bitcoin")
        self.assertContains(response, "BTC")

    def test_price_dynamics_1y_url(self):
        url = reverse("price-dynamics-for-1y")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_hedge_funds_url(self):
        url = reverse("hedge-funds")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Hedge Fund A")
        self.assertContains(response, "Hedge Fund B")
