from celery import shared_task
from .models import Subscription
from datetime import datetime


@shared_task()
def remove_expired_subscriptions():
    today = datetime.today()
    expired_subs = Subscription.objects.filter(expires_in__lt=today)

    if expired_subs.exists():
        deleted_count = 0
        for sub in expired_subs:
            sub.delete()
            sub.user_plan.delete()
            deleted_count += 1

        return f'{deleted_count} subscriptions deleted.'
    else:
        return 'No expired subscriptions to delete.'
