from fastapi import status
from fastapi.testclient import TestClient
from unittest.mock import patch

from app import models, exceptions
from tests.helpers import client, authenticate


@patch("app.daos.poems_dao.create_poem")
@patch("app.auth.get_current_user")
def test_create_poem_success(mock_get_current_user, mock_create_poem, client: TestClient):
    mock_get_current_user.return_value = models.User(id=1, email="user@example.com", name="Test User")
    mock_create_poem.return_value = models.Poem(id=1, title="Test Poem", content="This is a test poem", author_id=1)

    authenticate(client)
    response = client.post("/poems", json={"title": "Test Poem", "content": "This is a test poem"})

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test Poem"
    assert data["content"] == "This is a test poem"

    mock_create_poem.assert_called_once()



@patch("app.daos.poems_dao.count_poems")
@patch("app.daos.poems_dao.get_poems")
def test_list_poems_success(mock_get_poems, mock_count_poems, client: TestClient):
    mock_count_poems.return_value = 1
    mock_get_poems.return_value = [
        models.Poem(id=1, title="Poem 1", content="Content 1", author_id=1),
        models.Poem(id=2, title="Poem 2", content="Content 2", author_id=1)
    ]

    response = client.get("/poems")
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 2
    assert data["poems"][0]["title"] == "Poem 1"
    assert data["poems"][1]["title"] == "Poem 2"
    assert data["total_pages"] == 1

    mock_get_poems.assert_called_once()


@patch("app.daos.poems_dao.get_poems_by_author")
@patch("app.daos.poems_dao.count_poems_by_author")
@patch("app.auth.get_current_user")
def test_list_my_poems_success(
    mock_get_current_user, mock_count_poems_by_author,
    mock_get_poems_by_author, client: TestClient):
    mock_count_poems_by_author.return_value = 2
    mock_get_current_user.return_value = models.User(id=1, email="user@example.com", name="Test User")
    mock_get_poems_by_author.return_value = [
        models.Poem(id=1, title="Poem 1", content="Content 1", author_id=1),
        models.Poem(id=2, title="Poem 2", content="Content 2", author_id=1)
    ]

    response = client.get("/my/poems")
    
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 2
    assert data["poems"][0]["title"] == "Poem 1"
    assert data["poems"][1]["title"] == "Poem 2"
    assert data["total_pages"] == 1

    mock_get_poems_by_author.assert_called_once()


@patch("app.daos.poems_dao.get_poem_by_id")
@patch("app.auth.get_current_user")
def test_get_poem_success(mock_get_current_user, mock_get_poem_by_id, client: TestClient):
    mock_get_current_user.return_value = models.User(id=1, email="user@example.com", name="Test User")
    mock_get_poem_by_id.return_value = models.Poem(id=1, title="Test Poem", content="This is a test poem", author_id=1)

    response = client.get("/poems/1")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test Poem"
    assert data["content"] == "This is a test poem"
    assert "author" in data

    mock_get_poem_by_id.assert_called_once()


@patch("app.daos.poems_dao.get_poem_by_id")
@patch("app.auth.get_current_user")
def test_get_poem_not_found(mock_get_current_user, mock_get_poem_by_id, client: TestClient):
    mock_get_current_user.return_value = models.User(id=1, email="user@example.com", name="Test User")
    mock_get_poem_by_id.return_value = None

    response = client.get("/poems/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["detail"] == "Poem not found"

    mock_get_poem_by_id.assert_called_once()


@patch("app.daos.poems_dao.drop_poem")
@patch("app.auth.get_current_user")
def test_delete_poem_success(mock_get_current_user, mock_drop_poem, client: TestClient):
    mock_get_current_user.return_value = models.User(id=1, email="user@example.com", name="Test User")

    response = client.delete("/poems/1")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    mock_drop_poem.assert_called_once()


@patch("app.daos.poems_dao.drop_poem")
@patch("app.auth.get_current_user")
def test_delete_poem_forbidden(mock_get_current_user, mock_drop_poem, client: TestClient):
    mock_get_current_user.return_value = models.User(id=1, email="user@example.com", name="Test User")
    mock_drop_poem.side_effect = exceptions.PoemForbiddenException()

    response = client.delete("/poems/1")

    assert response.status_code == status.HTTP_403_FORBIDDEN
    data = response.json()
    assert data["detail"] == "You don't have permission to delete this poem"

    mock_drop_poem.assert_called_once()


@patch("app.daos.poems_dao.update_poem")
@patch("app.auth.get_current_user")
def test_update_poem_success(mock_get_current_user, mock_update_poem, client: TestClient):
    mock_get_current_user.return_value = models.User(id=1, email="user@example.com", name="Test User")
    mock_update_poem.return_value = models.Poem(id=1, title="Updated Title", content="Updated Content", author_id=1)

    response = client.put("/poems/1", json={"title": "Updated Title", "content": "Updated Content"})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Updated Title"
    assert data["content"] == "Updated Content"

    mock_update_poem.assert_called_once()


@patch("app.daos.poems_dao.update_poem")
@patch("app.auth.get_current_user")
def test_update_poem_forbidden(mock_get_current_user, mock_update_poem, client: TestClient):
    mock_get_current_user.return_value = models.User(id=1, email="user@example.com", name="Test User")
    mock_update_poem.side_effect = exceptions.PoemForbiddenException()

    response = client.put("/poems/1", json={"title": "Updated Title", "content": "Updated Content"})

    assert response.status_code == status.HTTP_403_FORBIDDEN
    data = response.json()
    assert data["detail"] == "You don't have permission to update this poem"

    mock_update_poem.assert_called_once()
