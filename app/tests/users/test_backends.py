# This work is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
# https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode


import pytest
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from users.backends import CustomAuthBackend

UserModel = get_user_model()


@pytest.mark.django_db
def test_authenticate_success():
    backend = CustomAuthBackend()
    email = "test@example.com"
    password = "testpassword123"
    UserModel.objects.create_user(email=email, password=password)

    authenticated_user = backend.authenticate(
        request=None, email=email, password=password
    )
    assert authenticated_user is not None
    assert authenticated_user.email == email


@pytest.mark.django_db
def test_authenticate_failure_wrong_password():
    backend = CustomAuthBackend()
    email = "test@example.com"
    password = "testpassword123"
    wrong_password = "wrongpassword"
    UserModel.objects.create_user(email=email, password=password)

    authenticated_user = backend.authenticate(
        request=None, email=email, password=wrong_password
    )
    assert authenticated_user is None


@pytest.mark.django_db
def test_authenticate_failure_no_user():
    backend = CustomAuthBackend()
    email = "nonexistent@example.com"
    password = "testpassword123"

    authenticated_user = backend.authenticate(
        request=None, email=email, password=password
    )
    assert authenticated_user is None


@pytest.mark.django_db
def test_get_user_success():
    backend = CustomAuthBackend()
    email = "test@example.com"
    password = "testpassword123"
    user = UserModel.objects.create_user(email=email, password=password)

    retrieved_user = backend.get_user(user_id=user.id)
    assert retrieved_user is not None
    assert retrieved_user.email == email


@pytest.mark.django_db
def test_get_user_failure():
    backend = CustomAuthBackend()

    retrieved_user = backend.get_user(user_id=999)
    assert retrieved_user is None
