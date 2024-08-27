from celery import shared_task
from django.utils import timezone
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken


@shared_task
def delete_expired_refresh_tokens():
    try:
        now = timezone.now()
        OutstandingToken.objects.filter(expires_at__lte=now).delete()
        print("Expired refresh tokens are deleted")

    except Exception as e:
        print(f"Error during deleting tokens: {str(e)}")
