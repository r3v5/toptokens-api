from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path("logout/", views.LogoutAPIView.as_view(), name="logout"),
    path(
        "signup/",
        views.SignupAPIView.as_view(),
        name="signup",
    ),
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path(
        "token/verify/",
        views.VerifyRefreshTokenAPIView.as_view(),
        name="token-verify",
    ),
    path(
        "token/delete-tokens-with-none-users/",
        views.DeleteRefreshTokenWithNoneUserAPIView.as_view(),
        name="token-delete",
    ),
    path(
        "token/delete-tokens-with-none-users/",
        views.DeleteRefreshTokenAPIView.as_view(),
        name="token-delete",
    ),
    path("profile/", views.UserAPIView.as_view(), name="profile"),
    path("delete-profile/", views.UserAPIView.as_view(), name="delete-user"),
]
