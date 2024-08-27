from django.db import models


class HedgeFund(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)

    def __str__(self) -> str:
        return self.name


class Cryptocurrency(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)
    ticker = models.CharField(max_length=20, blank=False, null=False)
    price = models.FloatField(blank=False, null=False)
    market_cap = models.PositiveBigIntegerField(blank=False, null=False)
    hedge_funds = models.ManyToManyField(
        HedgeFund, blank=False, related_name="cryptocurrencies"
    )

    def __str__(self):
        return f"{self.ticker} - {self.name}"


class MarketIndicator(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)
    value = models.PositiveIntegerField(blank=False, null=False)

    def __str__(self):
        return f"{self.name}: {self.value}"


class MarketRecommendation(models.Model):
    RECOMMENDATION_TYPES = [
        ("buy", "Buy"),
        ("sell", "Sell"),
    ]

    type = models.CharField(
        max_length=10, choices=RECOMMENDATION_TYPES, blank=False, null=False
    )
    indicator_name = models.CharField(max_length=256, blank=False, null=False)
    value = models.PositiveIntegerField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.indicator_name} - {self.type.capitalize()} ({self.value})"
