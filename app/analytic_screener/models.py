from django.db import models


class HedgeFund(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)


def __str__(self):
    return self.name


class Cryptocurrency(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)
    ticker = models.CharField(max_length=20, blank=False, null=False)
    price = models.FloatField(blank=False, null=False)
    market_cap = models.PositiveBigIntegerField(blank=False, null=False)
    hedge_funds = models.ManyToManyField(
        HedgeFund, blank=False, related_name="cryptocurrencies"
    )
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
