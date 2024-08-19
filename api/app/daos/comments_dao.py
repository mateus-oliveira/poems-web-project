from sqlalchemy.orm import Session
from app import models


def get_comments_by_poem_id(db: Session, poem_id: int):
    return (
        db.query(models.Comment)
            .join(models.User, models.Comment.author_id == models.User.id)
            .filter(models.Comment.poem_id == poem_id)
            .all()
    )


def comment(db: Session, content: str, poem_id: int, author_id: int):
    db_comment = models.Comment(content=content, poem_id=poem_id, author_id=author_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment
