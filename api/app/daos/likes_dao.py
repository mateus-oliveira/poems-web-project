from sqlalchemy.orm import Session
from app import models, exceptions


def get_likes_by_poem_id(db: Session, poem_id: int):
    return db.query(models.Like).filter(models.Like.poem_id == poem_id).all()


def like(db: Session, poem_id: int, user_id: int):
    like = db.query(models.Like).filter(models.Like.poem_id == poem_id, models.Like.user_id == user_id).first()
    
    if like:
        db.delete(like)
        db.commit()
        return False
    
    db_like = models.Like(poem_id=poem_id, user_id=user_id)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return True
