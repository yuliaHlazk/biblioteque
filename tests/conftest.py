import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from api_app.models import Author, Publisher


@pytest.fixture(scope="function")
def api_client() -> APIClient:
    yield APIClient()


@pytest.fixture(scope="function")
def user(db) -> User:
    yield User.objects.create_user(
        username="adminuser",
        password="1234",
        email="adminuser@gmail.com",
        is_staff=True,
    )


@pytest.fixture(scope="function")
def author(db):
    yield Author.objects.create(name="Test Author")


@pytest.fixture(scope="function")
def publisher(db):
    yield Publisher.objects.create(name="Test Publisher")
