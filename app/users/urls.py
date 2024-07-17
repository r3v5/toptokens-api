# This work is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
# https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

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
    path("profile/", views.UserAPIView.as_view(), name="user"),
    path("delete-profile/", views.UserAPIView.as_view(), name="delete-user"),
]
