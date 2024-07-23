import pytest
from rest_framework.exceptions import ValidationError
from users.models import CustomUser
from users.serializers import ProfileSerializer, SignupSerializer


@pytest.mark.django_db
def test_signup_serializer_valid():
    data = {"email": "test@example.com", "password": "strongpassword"}
    serializer = SignupSerializer(data=data)
    assert serializer.is_valid()
    user = serializer.save()
    assert user.email == data["email"]
    assert user.check_password(data["password"])


@pytest.mark.django_db
def test_signup_serializer_invalid_password():
    data = {"email": "test@example.com", "password": "short"}
    serializer = SignupSerializer(data=data)
    with pytest.raises(ValidationError) as excinfo:
        serializer.is_valid(raise_exception=True)
    assert "Password must be at least 8 characters long" in str(excinfo.value)


@pytest.mark.django_db
def test_profile_serializer():
    user = CustomUser.objects.create_user(
        email="test@example.com", password="strongpassword"
    )
    serializer = ProfileSerializer(user)
    assert serializer.data == {
        "email": user.email,
        "date_joined": user.date_joined.strftime("%Y-%m-%d"),
    }
