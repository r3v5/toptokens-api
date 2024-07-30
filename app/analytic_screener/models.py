from django.db import models


class Cryptocurrency(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)
    ticker = models.CharField(max_length=20, blank=False, null=False)
    price = models.FloatField(blank=False, null=False)
    market_cap = models.PositiveBigIntegerField(blank=False, null=False)
    price_dynamics_for_1_year = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True
    )
    price_dynamics_for_6_months = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True
    )
    price_dynamics_for_3_months = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True
    )
    price_dynamics_for_1_month = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True
    )

    def __str__(self):
        return f"{self.ticker} - {self.name}"


class HedgeFund(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)
    cryptocurrencies = models.ManyToManyField(
        Cryptocurrency, blank=False, related_name="hedge_funds"
    )


def __str__(self):
    return self.name


class MarketIndicator(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)
    value = models.PositiveIntegerField(blank=False, null=False)

    def __str__(self):
        return f"{self.name}: {self.value}"
