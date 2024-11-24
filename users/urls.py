from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (PaymentListAPIView, UserCreateAPIView,
                         UserDestroyAPIView, UserListAPIView,
                         UserRetrieveAPIView, UserUpdateAPIView, SubscriptionAPIView)

app_name = UsersConfig.name

urlpatterns = [
    path("", UserListAPIView.as_view(), name="users_list"),
    path(
        "register/",
        UserCreateAPIView.as_view(permission_classes=[AllowAny]),
        name="register",
    ),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name="user_detail"),
    path("edit/<int:pk>/", UserUpdateAPIView.as_view(), name="user_edit"),
    path("delete/<int:pk>/", UserDestroyAPIView.as_view(), name="user_delete"),
    path("payment/", PaymentListAPIView.as_view(), name="user_payments"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=[AllowAny]),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=[AllowAny]),
        name="token_refresh",
    ),
    path("subs/", SubscriptionAPIView.as_view(), name="subscription"),
]
