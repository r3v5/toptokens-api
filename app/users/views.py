from typing import Dict

from django.contrib.auth import authenticate, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import exceptions, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import ProfileSerializer, SignupSerializer


def generate_tokens_for_user(user: CustomUser) -> Dict[str, str]:
    refresh = RefreshToken.for_user(user)
    return {
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh),
    }


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
            tokens = generate_tokens_for_user(user)

            user.is_active = True
            user.save()

            response = Response(
                tokens,
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

                if not refresh_token:
                    return Response(
                        {"message": "Refresh token is required."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                token = RefreshToken(refresh_token)
                refresh_token_jti = token["jti"]
                OutstandingToken.objects.filter(jti=refresh_token_jti).delete()
                request.user.is_active = False
                request.user.save()
                logout(request)

                return Response(
                    {"message": "Logout successfully"},
                    status=status.HTTP_205_RESET_CONTENT,
                )

            except Exception:
                return Response(
                    {"message": "An error occurred during logout."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(
            {"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
        )


class VerifyRefreshTokenAPIView(APIView):

    def post(self, request: HttpRequest) -> HttpResponse:
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return Response(
                {"message": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.verify()

            return Response(
                {"message": "Refresh token is valid."}, status=status.HTTP_200_OK
            )

        except TokenError:
            # Delete all expired refresh tokens
            now = timezone.now()
            OutstandingToken.objects.filter(expires_at__lte=now).delete()

            return Response(
                {"message": "Refresh token is invalid and has been revoked."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class DeleteRefreshTokenAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def delete(self, request: HttpRequest) -> HttpResponse:
        try:
            OutstandingToken.objects.filter(user=None).delete()

            return Response(
                {"message": "Tokens associated with Null users are deleted"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            return Response(
                {"message": f"Error during deleting tokens: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


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
