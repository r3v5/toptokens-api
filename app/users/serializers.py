# This work is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
# https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode


from typing import Any, Dict, Optional

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import CustomUser


def validate_password(value: str) -> str:
    if len(value) < 8:
        raise serializers.ValidationError("Password must be at least 8 characters long")
    return value


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    def create(self, validated_data: Dict[str, Any]) -> CustomUser:
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = CustomUser
        fields = ["id", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
        ]
