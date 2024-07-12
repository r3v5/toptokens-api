# This work is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
# https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

from typing import Any, Optional

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

if False:  # type checking
    from .models import CustomUser  # noqa


class CustomUserManager(BaseUserManager):
    def create_user(
        self, email: str, password: Optional[str] = None, **extra_fields: Any
    ) -> "CustomUser":
        from .models import CustomUser

        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email: str, password: Optional[str], **extra_fields: Any
    ) -> "CustomUser":
        from .models import CustomUser

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
