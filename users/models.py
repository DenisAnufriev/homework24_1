from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    phone = models.CharField(
        max_length=35, **NULLABLE, verbose_name="Телефон", help_text="Укажите телефон"
    )
    city = models.CharField(
        max_length=50, **NULLABLE, verbose_name="Город", help_text="Укажите ваш город"
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        **NULLABLE,
        verbose_name="Аватар",
        help_text="Загрузите аватар"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    class PayMethod(models.TextChoices):
        CASH = "cash", "Наличные"
        TRANSFER = "transfer", "Перевод на карту"

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="payments")
    lesson = models.ForeignKey(
        "lms.Lesson", on_delete=models.CASCADE, **NULLABLE, related_name="payments"
    )
    course = models.ForeignKey(
        "lms.Course", on_delete=models.CASCADE, **NULLABLE, related_name="payments"
    )

    pay_day = models.DateField(auto_now_add=True, verbose_name="Дата оплаты")
    pay_method = models.CharField(
        max_length=10,
        choices=PayMethod.choices,
        default=PayMethod.CASH,
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"


class Subscription(models.Model):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="subscriptions"
    )
    course = models.ForeignKey(
        "lms.Course", on_delete=models.CASCADE, related_name="subscriptions"
    )

    def __str__(self):
        return f"{self.user} signed {self.user}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
