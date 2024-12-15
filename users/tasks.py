from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def deactivate_inactive_users():
    """
    Деактивирует пользователей, не активных более 30 дней.

    Определяет пользователей, которые не заходили в систему в течение последних
    30 дней и имеют статус активного пользователя (is_active=True), и деактивирует их.
    """
    month = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lte=month, is_active=True)
    if inactive_users.exists():
        inactive_users.update(is_active=False)
        print(f"Пользователи деактивированы")
    else:
        print("Не активные пользователи не обнаружены.")
