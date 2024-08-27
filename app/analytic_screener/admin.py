from django.contrib import admin

from .models import Cryptocurrency, HedgeFund, MarketIndicator, MarketRecommendation


@admin.register(HedgeFund)
class HedgeFundAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Cryptocurrency)
class CryptocurrencyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "ticker",
        "price",
        "market_cap",
    )
    search_fields = (
        "name",
        "ticker",
    )
    list_filter = ("hedge_funds",)


@admin.register(MarketIndicator)
class MarketIndicatorAdmin(admin.ModelAdmin):
    list_display = ("name", "value")
    search_fields = ("name", "value")


@admin.register(MarketRecommendation)
class MarketRecommendationAdmin(admin.ModelAdmin):
    list_display = ("type", "indicator_name", "value", "created_at")
    list_filter = ("type", "indicator_name")
    search_fields = ("indicator_name", "value")
    ordering = ("-created_at",)
