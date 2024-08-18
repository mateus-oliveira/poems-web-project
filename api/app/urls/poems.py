from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, database, daos, exceptions, auth


router = APIRouter()


@router.post("/poems")
async def create_poem(
    poem: models.PoemCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    db_poem = daos.poems_dao.create_poem(db, poem, current_user.id)
    return db_poem


@router.post("/poems")
async def create_poem(
    poem: models.PoemCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    db_poem = daos.poems_dao.create_poem(db, poem, current_user.id)
    return db_poem


@router.delete("/poems/{poem_id}")
async def get_poems(
    poem_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)):
    try:
        daos.poems_dao.drop_poem(db, poem_id, current_user.id)
    except exceptions.PoemDeleteForbiddenException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You don't have permission to delete this poem")
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    else:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/poems/{poem_id}")
async def update_poem(
    poem_id: int,
    poem: models.PoemCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    db_poem = daos.poems_dao.get_poem_by_id(db, poem_id)
    if not db_poem or db_poem.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Poem not found or you do not have permission to edit this poem")

    updated_poem = daos.poems_dao.update_poem(db, poem_id, poem.title, poem.content)
    return updated_poem
