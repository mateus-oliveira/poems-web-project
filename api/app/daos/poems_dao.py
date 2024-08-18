from sqlalchemy.orm import Session
from app import models


def create_poem(db: Session, poem: models.PoemCreate, author_id: int):
    db_poem = models.Poem(title=poem.title, content=poem.content, author_id=author_id)
    db.add(db_poem)
    db.commit()
    db.refresh(db_poem)
    return db_poem


def get_poems(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Poem).offset(skip).limit(limit).all()


def get_poem_by_id(db: Session, poem_id: int):
    return db.query(models.Poem).filter(models.Poem.id == poem_id).first()


def update_poem(db: Session, poem_id: int, title: str, content: str):
    db_poem = get_poem_by_id(db, poem_id)
    if db_poem:
        db_poem.title = title
        db_poem.content = content
        db.commit()
        db.refresh(db_poem)
    return db_poem
