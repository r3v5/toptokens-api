import pytest
from django.utils.translation import gettext_lazy as _
from users.managers import CustomUserManager


@pytest.mark.django_db
def test_create_user_no_email():

    manager = CustomUserManager()
    with pytest.raises(ValueError) as excinfo:
        manager.create_user(email=None, password="testpassword123")
    assert str(excinfo.value) == _("The Email must be set")


@pytest.mark.django_db
def test_create_superuser_no_is_staff():

    manager = CustomUserManager()
    email = "admin@example.com"
    password = "adminpassword123"
    with pytest.raises(ValueError) as excinfo:
        manager.create_superuser(email=email, password=password, is_staff=False)
    assert str(excinfo.value) == _("Superuser must have is_staff=True.")


@pytest.mark.django_db
def test_create_superuser_no_is_superuser():

    manager = CustomUserManager()
    email = "admin@example.com"
    password = "adminpassword123"
    with pytest.raises(ValueError) as excinfo:
        manager.create_superuser(email=email, password=password, is_superuser=False)
    assert str(excinfo.value) == _("Superuser must have is_superuser=True.")
