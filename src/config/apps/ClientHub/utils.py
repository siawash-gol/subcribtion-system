from config.apps.ClientHub.models import Plan, UserPlan, PayHistory
from config.auth.Users.models import User


def handel_subscribtion(payment_id, user_id, plan, amount):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise ValueError("User matching the given ID does not exist.")

    userplan, created = UserPlan.objects.update_or_create(
        user=user,
        defaults={
            'plan': plan,
            'payment_id': payment_id,
            'amount': amount,
            'status': True,
        }
    )
    return userplan
