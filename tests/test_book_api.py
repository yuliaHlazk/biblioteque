import pytest
from django.urls import reverse
from api_app.models import Book


@pytest.mark.django_db
def test_get_books_list(api_client, author, publisher) -> None:
    Book.objects.create(
        title="Book6", genre="novel", price="13.33",
        author=author, publisher=publisher
    )
    response = api_client.get("/api/books/", format="json")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0].get("title") == "Book6"


@pytest.mark.django_db
def test_get_books_empty_list(api_client) -> None:
    response = api_client.get("/api/books/", format="json")
    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_post_book_valid(api_client, user, author, publisher) -> None:
    login_url = reverse("token_obtain_pair")
    tokens = api_client.post(
        login_url, {"username": "adminuser", "password": "1234"}, format="json"
    ).data

    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
    response = api_client.post(
        "/api/books/",
        {
            "title": "new book",
            "genre": "novel",
            "price": "13.33",
            "author": author.id,
            "publisher": publisher.id,
        },
        format="json"
    )
    assert response.status_code in (201, 403)
    if response.status_code == 201:
        assert response.data["title"] == "new book"


@pytest.mark.django_db
def test_post_book_no_auth(api_client, author, publisher) -> None:
    data = {
        "title": "unauthorized book",
        "genre": "novel",
        "price": "13.33",
        "author": author.id,
        "publisher": publisher.id,
    }
    response = api_client.post("/api/books/", data, format="json")
    assert response.status_code in (401, 403)


@pytest.mark.django_db
def test_post_book_invalid_token(api_client, author, publisher) -> None:
    api_client.credentials(HTTP_AUTHORIZATION="Bearer invalidtoken")
    response = api_client.post(
        "/api/books/",
        {
            "title": "Fake Book",
            "genre": "novel",
            "price": "13.33",
            "author": author.id,
            "publisher": publisher.id,
        },
        format="json"
    )
    assert response.status_code in (401, 403)


@pytest.mark.django_db
def test_post_book_invalid_fields(api_client, user, author, publisher) -> None:
    login_url = reverse("token_obtain_pair")
    tokens = api_client.post(
        login_url, {"username": "adminuser", "password": "1234"}, format="json"
    ).data
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
    pure_data = {"title": "lala", "genre": "some random", "price": "", "author": ""}
    
    response = api_client.post("/api/books/", pure_data, format="json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_get_book_detail_with_auth(api_client, user, author, publisher) -> None:
    login_url = reverse("token_obtain_pair")
    tokens = api_client.post(
        login_url, {"username": "adminuser", "password": "1234"}, format="json"
    ).data
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')

    book = Book.objects.create(
        title="see the book", genre="novel", price="13.33",
        author=author, publisher=publisher
    )
    
    response = api_client.get(f"/api/books/{book.id}/", format="json")
    assert response.status_code in (200, 403, 401)


@pytest.mark.django_db
def test_get_book_detail_no_auth(api_client, author, publisher) -> None:
    book = Book.objects.create(
        title="hidden book", genre="novel", price="13.33",
        author=author, publisher=publisher
    )
    response = api_client.get(f"/api/books/{book.id}/", format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_get_book_detail_not_found(api_client, user) -> None:
    login_url = reverse("token_obtain_pair")
    tokens = api_client.post(
        login_url, {"username": "adminuser", "password": "1234"}, format="json"
    ).data
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
    response = api_client.get("/api/books/777/", format="json")
    assert response.status_code == 404


@pytest.mark.django_db
def test_put_book_as_admin(api_client, user, author, publisher) -> None:
    login_url = reverse("token_obtain_pair")
    tokens = api_client.post(
        login_url, {"username": "adminuser", "password": "1234"}, format="json"
    ).data
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')

    book = Book.objects.create(
        title="old", genre="novel", price="13.33",
        author=author, publisher=publisher
    )
    data = {"title": "updated", "genre": "novel", "price": "33.33",
            "author": author.id, "publisher": publisher.id}
    response = api_client.put(f"/api/books/{book.id}/", data, format="json")
    assert response.status_code in (200, 403)
    
    if response.status_code == 200:
        assert response.data["title"] == "updated"


@pytest.mark.django_db
def test_put_book_not_found(api_client, user, author, publisher) -> None:
    login_url = reverse("token_obtain_pair")
    tokens = api_client.post(
        login_url, {"username": "adminuser", "password": "1234"}, format="json"
    ).data
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')

    data = {"title": "non exist", "genre": "novel", "price": "13.33",
            "author": author.id, "publisher": publisher.id}
    response = api_client.put("/api/books/777/", data, format="json")
    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_book_no_auth(api_client, author, publisher) -> None:
    book = Book.objects.create(
        title="unauthorized delete", genre="novel", price="13.33",
        author=author, publisher=publisher
    )
    response = api_client.delete(f"/api/books/{book.id}/", format="json")
    assert response.status_code in (401, 403)
    

@pytest.mark.django_db
def test_delete_book_as_admin(api_client, user, author, publisher) -> None:
    login_url = reverse("token_obtain_pair")
    tokens = api_client.post(
        login_url, {"username": "adminuser", "password": "1234"}, format="json"
    ).data
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')

    book = Book.objects.create(
        title="delete", genre="novel", price="13.33",
        author=author, publisher=publisher
    )
    response = api_client.delete(f"/api/books/{book.id}/", format="json")
    assert response.status_code in (200, 403)


@pytest.mark.django_db
def test_delete_book_not_found(api_client, user) -> None:
    login_url = reverse("token_obtain_pair")
    tokens = api_client.post(
        login_url, {"username": "adminuser", "password": "1234"}, format="json"
    ).data
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')
    response = api_client.delete("/api/books/777/", format="json")
    assert response.status_code == 404
