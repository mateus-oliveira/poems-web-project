from app.config import database
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import models, daos, auth


router = APIRouter()


@router.post("/poems/{poem_id}/likes", status_code=status.HTTP_201_CREATED)
async def create_poem(
    poem_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    liked = daos.likes_dao.like(db, poem_id, current_user.id)
    return {'liked': liked}


@router.get("/poems/{poem_id}/likes")
async def get_likes(
    poem_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    likes = daos.likes_dao.get_likes_by_poem_id(db, poem_id)
    if not likes:
        return []
    return likes
