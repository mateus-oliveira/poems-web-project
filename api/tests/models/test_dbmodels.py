import pytest
from app.models import User

from tests.helpers import db


def test_create_user(db):
    user = User(email="test@example.com", name="Test User", password="hashed_password")
    db.add(user)
    db.commit()

    saved_user = db.query(User).filter_by(email="test@example.com").first()
    assert saved_user is not None
    assert saved_user.email == "test@example.com"
    assert saved_user.name == "Test User"
    assert saved_user.password == "hashed_password"


def test_create_user_with_duplicate_email(db):
    user1 = User(email="duplicate@example.com", name="User One", password="password1")
    db.add(user1)
    db.commit()

    user2 = User(email="duplicate@example.com", name="User Two", password="password2")
    db.add(user2)

    with pytest.raises(Exception):
        db.commit()


def test_create_user_without_name(db):
    user = User(email="noname@example.com", password="password")
    db.add(user)

    db.commit()
    saved_user = db.query(User).filter_by(email="noname@example.com").first()
    assert saved_user is not None
    assert saved_user.name is None
