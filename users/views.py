from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course
from users.models import User, Payment, Subscription
from users.serializers import (
    UserSerializer,
    PaymentSerializer,
    UserPublicSerializer,
    SubscriptionSerializer,
)
from users.services import (
    create_stripe_session,
    create_stripe_price,
    convert_rub_to_usd, create_stripe_product,
)


class UserCreateAPIView(generics.CreateAPIView):
    """
    Представление для создания нового пользователя.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """
        Сохраняет нового пользователя со статусом "активен".
        Если указан пароль, он хэшируется и сохраняется.
        """
        user = serializer.save(is_active=True)
        password = self.request.data.get("password")
        if password:
            user.set_password(password)
            user.save()


class UserListAPIView(generics.ListAPIView):
    """
    Представление для получения списка всех пользователей.
    """

    queryset = User.objects.all()
    serializer_class = UserPublicSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    """
    Представление для обновления профиля текущего пользователя.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_update(self, serializer):
        """
        Обновляет профиль пользователя. Если указан новый пароль, он хэшируется.
        Выдает PermissionDenied, если пользователь пытается изменить чужой профиль.
        """
        if serializer.instance != self.request.user:
            raise PermissionDenied("У вас нет прав что бы изменять этот профиль.")

        user = serializer.save()

        new_password = self.request.data.get("password")
        if new_password:
            user.set_password(new_password)
        user.save()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """
    Представление для получения информации о конкретном пользователе.
    """

    queryset = User.objects.all()
    serializer_class = UserPublicSerializer

    def get_serializer_class(self):
        if getattr(self, "swagger_fake_view", False):
            return UserSerializer

        # Обычная логика выполнения
        if self.get_object() == self.request.user:
            return UserSerializer
        return UserPublicSerializer


class UserDestroyAPIView(generics.DestroyAPIView):
    """
    Представление для удаления профиля текущего пользователя.
    """

    queryset = User.objects.all()
    serializer_class = UserPublicSerializer

    def perform_destroy(self, instance):
        """
        Удаляет профиль пользователя. Выдает PermissionDenied, если пользователь пытается
        удалить чужой профиль.
        """
        if instance != self.request.user:
            raise PermissionDenied(
                "У вас недостаточно прав что бы удалить этого пользователя."
            )
        instance.delete()


class SubscriptionAPIView(APIView):
    """
    Представление для управления подписками пользователя на курсы.
    """

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
        """
        Переключает статус подписки пользователя на указанный курс.
        Возвращает сообщение о добавлении или удалении подписки.
        """
        user = request.user
        course_id = request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)
        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"
        return Response({"message": message}, status=status.HTTP_200_OK)


class PaymentCreateAPIView(CreateAPIView):
    """
    Представление для создания платежа и формирования Stripe-сессии для обработки.
    """

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        """
        Сохраняет платеж, конвертирует сумму в USD, создает объект цены в Stripe
        и генерирует Stripe-сессию. Сохраняет идентификатор сессии и ссылку на оплату.
        """
        payment = serializer.save(user=self.request.user)

        amount_in_usd = convert_rub_to_usd(payment.amount)

        course = Course.objects.get(id=payment.course.id)
        name = course.title
        product = create_stripe_product(name)
        price = create_stripe_price(amount_in_usd, product)

        session_id, payment_link = create_stripe_session(price)

        payment.session_id = session_id
        payment.link = payment_link
        payment.save()
