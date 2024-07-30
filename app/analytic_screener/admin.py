from django.contrib import admin

from .models import Cryptocurrency, HedgeFund, MarketIndicator


@admin.register(HedgeFund)
class HedgeFundAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Cryptocurrency)
class CryptocurrencyAdmin(admin.ModelAdmin):
    list_display = ("name", "ticker", "price", "market_cap")
    list_filter = (
        "price_dynamics_for_1_year",
        "price_dynamics_for_6_months",
        "price_dynamics_for_3_months",
        "price_dynamics_for_1_month",
    )
    search_fields = ("name", "ticker")
    filter_horizontal = ("hedge_funds",)


@admin.register(MarketIndicator)
class MarketIndicatorAdmin(admin.ModelAdmin):
    list_display = ("name", "value")
    search_fields = ("name", "value")
