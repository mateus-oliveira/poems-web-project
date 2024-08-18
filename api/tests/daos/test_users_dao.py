import pytest

from app import models, exceptions
from app.daos import users_dao

from tests.helpers import db



def test_get_user_by_email(db):
    db_user = models.User(email="test@example.com", name="Test User", password="hashed_password")
    db.add(db_user)
    db.commit()

    user = users_dao.get_user_by_email(db, email="test@example.com")
    assert user is not None
    assert user.email == "test@example.com"


def test_create_user(db):
    new_user = models.UserCreate(email="new@example.com", name="New User", password="new_password")
    created_user = users_dao.create_user(db, user=new_user, hashed_password="hashed_new_password")

    assert created_user is not None
    assert created_user.email == "new@example.com"
    assert created_user.password == "hashed_new_password"

    with pytest.raises(exceptions.UserEmailException):
        users_dao.create_user(db, user=new_user, hashed_password="another_hashed_password")


def test_get_user_by_id(db):
    db_user = models.User(email="test@example.com", name="Test User", password="hashed_password")
    db.add(db_user)
    db.commit()

    user = users_dao.get_user_by_id(db, user_id=db_user.id)
    assert user is not None
    assert user.id == db_user.id

    assert users_dao.get_user_by_id(db, user_id=999) is None
