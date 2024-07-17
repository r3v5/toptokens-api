# This work is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
# https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

from django.conf import settings
from django.contrib.auth import authenticate, logout
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import exceptions, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import ProfileSerializer, SignupSerializer


class SignupAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request: HttpRequest) -> HttpResponse:
        if request.data["password"] != request.data["password_confirm"]:
            response = {
                "message": "Passwords do not match",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request: HttpRequest) -> HttpResponse:
        email = request.data["email"]
        password = request.data["password"]

        user = CustomUser.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed("Invalid credentials")

        elif not user.check_password(password):
            raise exceptions.AuthenticationFailed("Invalid credentials")

        else:

            user = authenticate(request, email=email, password=password)
            access_token = str(RefreshToken.for_user(user).access_token)
            refresh_token = str(RefreshToken.for_user(user))

            user.is_active = True
            user.save()

            response = Response(
                {"access_token": access_token, "refresh_token": refresh_token},
                status=status.HTTP_200_OK,
            )

            return response


class LogoutAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:

            try:
                refresh_token = request.data["refresh_token"]
                token = RefreshToken(refresh_token)
                token.blacklist()
                request.user.is_active = False
                request.user.save()
                logout(request)
                response = Response(
                    {"message": "Logout successfully"},
                    status=status.HTTP_205_RESET_CONTENT,
                )
                return response

            except Exception:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_401_UNAUTHORIZED)


class UserAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest) -> HttpResponse:
        custom_user = get_object_or_404(CustomUser, pk=request.user.id)
        return Response(ProfileSerializer(custom_user).data, status=status.HTTP_200_OK)

    def delete(self, request: HttpRequest) -> HttpResponse:
        user = get_object_or_404(CustomUser, pk=request.user.id)
        user.delete()

        response = {
            "status": status.HTTP_204_NO_CONTENT,
            "message": "Profile deleted successfully",
        }

        return Response(response, status=status.HTTP_204_NO_CONTENT)
