from fastapi import status
from fastapi.testclient import TestClient
from unittest.mock import patch

from app import models, exceptions
from tests.helpers import client


@patch("app.daos.users_dao.create_user")
def test_register_user_success(mock_create_user, client: TestClient):
    mock_create_user.return_value = models.User(id=1, email="newuser@example.com", name="New User")

    response = client.post("/register", json={
        "email": "newuser@example.com",
        "name": "New User",
        "password": "password123"
    })

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["id"] == 1
    assert data["email"] == "newuser@example.com"
    assert data["name"] == "New User"

    mock_create_user.assert_called_once()


@patch("app.daos.users_dao.create_user")
def test_register_user_email_already_used(mock_create_user, client: TestClient):
    mock_create_user.side_effect = exceptions.UserEmailException()

    response = client.post("/register", json={
        "email": "existinguser@example.com",
        "name": "Another User",
        "password": "password123"
    })

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert data["detail"] == "Email already used"

    mock_create_user.assert_called_once()


@patch("app.daos.users_dao.get_user_by_email")
@patch("app.auth.verify_password")
@patch("app.auth.create_access_token")
def test_login_success(mock_create_access_token, mock_verify_password, mock_get_user_by_email, client: TestClient):
    mock_get_user_by_email.return_value = models.User(id=1, email="sampleuser@example.com", name="Sample User",
                                                      password="hashed_password")
    mock_verify_password.return_value = True
    mock_create_access_token.return_value = "testtoken"

    response = client.post("/login", json={
        "email": "sampleuser@example.com",
        "password": "password123"
    })

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["access_token"] == "testtoken"
    assert data["token_type"] == "Bearer"
    assert data["user"]["id"] == 1
    assert data["user"]["email"] == "sampleuser@example.com"
    assert data["user"]["name"] == "Sample User"

    mock_get_user_by_email.assert_called_once()
    mock_verify_password.assert_called_once()
    mock_create_access_token.assert_called_once()


@patch("app.daos.users_dao.get_user_by_email")
@patch("app.auth.verify_password")
def test_login_incorrect_password(mock_verify_password, mock_get_user_by_email, client: TestClient):
    mock_get_user_by_email.return_value = models.User(id=1, email="sampleuser@example.com", name="Sample User",
                                                      password="hashed_password")
    mock_verify_password.return_value = False

    response = client.post("/login", json={
        "email": "sampleuser@example.com",
        "password": "wrongpassword"
    })

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert data["detail"] == "Incorrect email or password"

    mock_get_user_by_email.assert_called_once()
    mock_verify_password.assert_called_once()


@patch("app.daos.users_dao.get_user_by_email")
def test_login_non_existent_user(mock_get_user_by_email, client: TestClient):
    mock_get_user_by_email.return_value = None

    response = client.post("/login", json={
        "email": "nonexistent@example.com",
        "password": "password123"
    })

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert data["detail"] == "Incorrect email or password"

    mock_get_user_by_email.assert_called_once()
