import pytest
from django.db import IntegrityError
from django.utils import timezone
from users.models import CustomUser


@pytest.mark.django_db
def test_create_user():
    user = CustomUser.objects.create_user(
        email="test@example.com", password="testpassword123"
    )
    assert user.email == "test@example.com"
    assert user.check_password("testpassword123")
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser
    assert isinstance(user.date_joined, timezone.datetime)


@pytest.mark.django_db
def test_create_user_no_email():
    with pytest.raises(ValueError, match="The Email must be set"):
        CustomUser.objects.create_user(email="", password="testpassword123")


@pytest.mark.django_db
def test_create_user_duplicate_email():
    CustomUser.objects.create_user(email="test@example.com", password="testpassword123")
    with pytest.raises(IntegrityError):
        CustomUser.objects.create_user(
            email="test@example.com", password="anotherpassword"
        )


@pytest.mark.django_db
def test_create_superuser():
    superuser = CustomUser.objects.create_superuser(
        email="admin@example.com", password="adminpassword123"
    )
    assert superuser.email == "admin@example.com"
    assert superuser.check_password("adminpassword123")
    assert superuser.is_active
    assert superuser.is_staff
    assert superuser.is_superuser
    assert isinstance(superuser.date_joined, timezone.datetime)


@pytest.mark.django_db
def test_create_superuser_no_is_staff():
    with pytest.raises(ValueError, match="Superuser must have is_staff=True."):
        CustomUser.objects.create_superuser(
            email="admin@example.com", password="adminpassword123", is_staff=False
        )


@pytest.mark.django_db
def test_create_superuser_no_is_superuser():
    with pytest.raises(ValueError, match="Superuser must have is_superuser=True."):
        CustomUser.objects.create_superuser(
            email="admin@example.com", password="adminpassword123", is_superuser=False
        )


@pytest.mark.django_db
def test_user_str():
    user = CustomUser.objects.create_user(
        email="test@example.com", password="testpassword123"
    )
    assert str(user) == "test@example.com"
