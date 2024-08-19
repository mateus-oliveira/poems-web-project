from app.config import database
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import models, daos, auth


router = APIRouter()


@router.post("/poems/{poem_id}/comments", status_code=status.HTTP_201_CREATED)
async def create_poem(
    comment: models.CommentCreate,
    poem_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    return daos.comments_dao.comment(db, comment.content, poem_id, current_user.id)


@router.get("/poems/{poem_id}/comments")
async def get_comments(
    poem_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    comments = daos.get_comments_by_poem_id(db, poem_id)
    return [
        models.CommentWithAuthor(
            id=comment.id,
            content=comment.content,
            author=models.Author(
                id=comment.author.id,
                name=comment.author.name,
                email=comment.author.email
            )
        )
        for comment in comments
    ]
