import os

from celery import Celery
from celery.schedules import crontab, timedelta
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")
app.config_from_object("django.conf:settings")
app.conf.broker_url = settings.CELERY_BROKER_URL
app.conf.broker_connection_retry_on_startup = os.environ.get(
    "CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP", "True"
).lower() in ("true", "1", "yes")

# Configure Celery Beat
app.conf.beat_schedule = {
    "parse_tier_1_portfolios": {
        "task": "analytic_screener.tasks.parse_tier_1_portfolios",
        "schedule": timedelta(seconds=20),
    },
    "update_fear_and_greed_indices": {
        "task": "analytic_screener.tasks.update_fear_and_greed_indices",
        "schedule": timedelta(seconds=20),
    },
}

app.autodiscover_tasks()
