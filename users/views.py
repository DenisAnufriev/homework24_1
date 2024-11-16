from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer, UserPublicSerializer


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        password = self.request.data.get("password")
        if password:
            user.set_password(password)
            user.save()


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserPublicSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_update(self, serializer):
        if serializer.instance != self.request.user:
            raise PermissionDenied("У вас нет прав что бы изменять этот профиль.")

        user = serializer.save()

        new_password = self.request.data.get("password")
        if new_password:
            user.set_password(new_password)
        user.save()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserPublicSerializer

    def get_serializer_class(self):
        if self.get_object() == self.request.user:
            return UserSerializer
        return UserPublicSerializer


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserPublicSerializer

    def perform_destroy(self, instance):
        if instance != self.request.user:
            raise PermissionDenied("У вас недостаточно прав что бы удалить этого пользователя.")
        instance.delete()


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ("pay_day",)
    filterset_fields = ("course", "lesson", "pay_method")
