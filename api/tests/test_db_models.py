import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, User


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


def test_create_user(db_session):
    user = User(email="test@example.com", name="Test User", password="hashed_password")
    db_session.add(user)
    db_session.commit()

    saved_user = db_session.query(User).filter_by(email="test@example.com").first()
    assert saved_user is not None
    assert saved_user.email == "test@example.com"
    assert saved_user.name == "Test User"
    assert saved_user.password == "hashed_password"


def test_create_user_with_duplicate_email(db_session):
    user1 = User(email="duplicate@example.com", name="User One", password="password1")
    db_session.add(user1)
    db_session.commit()

    user2 = User(email="duplicate@example.com", name="User Two", password="password2")
    db_session.add(user2)

    with pytest.raises(Exception):
        db_session.commit()


def test_create_user_without_name(db_session):
    user = User(email="noname@example.com", password="password")
    db_session.add(user)

    db_session.commit()
    saved_user = db_session.query(User).filter_by(email="noname@example.com").first()
    assert saved_user is not None
    assert saved_user.name is None
