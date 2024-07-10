from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models


class CustomUser(AbstractBaseUser, PermissionsMixin):
    pass
