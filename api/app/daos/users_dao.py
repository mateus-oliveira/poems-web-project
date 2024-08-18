from sqlalchemy.orm import Session
from app import models, exceptions


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: models.UserCreate, hashed_password: str):
    old_user = get_user_by_email(db, user.email)

    if old_user:
        raise exceptions.UserEmailException()

    db_user = models.User(email=user.email, name=user.name, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()
