import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")


app = Celery("core")
app.config_from_object("django.conf:settings")
app.conf.broker_url = settings.CELERY_BROKER_URL
app.conf.broker_connection_retry_on_startup = os.environ.get(
    "CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP", "True"
).lower() in ("true", "1", "yes")

# # Configure Celery Beat
# app.conf.beat_schedule = {
#     "update-event-status": {
#         "task": "content.tasks.update_event_status",
#         "schedule": crontab(minute="*/5"),
#     },
#     "check_event_started": {
#         "task": "content.tasks.check_event_started",
#         "schedule": crontab(minute="*/5"),
#     },
# }


# app.autodiscover_tasks()
