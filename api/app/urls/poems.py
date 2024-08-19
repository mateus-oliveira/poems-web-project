from app.config import database
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from app import models, daos, exceptions, auth


router = APIRouter()


@router.post("/poems", status_code=status.HTTP_201_CREATED)
async def create_poem(
    poem: models.PoemCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    db_poem = daos.poems_dao.create_poem(db, poem, current_user.id)
    return db_poem


@router.delete("/poems/{poem_id}")
async def delete_poem(
    poem_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    try:
        daos.poems_dao.drop_poem(db, poem_id, current_user.id)
    except exceptions.PoemForbiddenException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this poem")
    except exceptions.NotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Poem not found")
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error")
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/poems/{poem_id}")
async def update_poem(
    poem_id: int,
    poem: models.PoemCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    try:
        updated_poem = daos.poems_dao.update_poem(db, poem_id, poem.title, poem.content, author_id=current_user.id)
        return updated_poem
    except exceptions.PoemForbiddenException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this poem")
    except exceptions.NotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Poem not found")
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error")


@router.get("/poems")
async def list_poems(
    skip: int = 0,
    limit: int = 10,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    total_poems = daos.poems_dao.count_poems(db)
    poems = daos.poems_dao.get_poems(db, skip=skip, limit=limit)
    total_pages = (total_poems + limit - 1) // limit

    return {
        "poems": poems,
        "total_pages": total_pages
    }


@router.get("/my/poems")
async def list_poems(
    skip: int = 0,
    limit: int = 10,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    total_poems = daos.poems_dao.count_poems_by_author(db, current_user.id)
    poems = daos.poems_dao.get_poems_by_author(db, current_user.id, skip=skip, limit=limit)
    total_pages = (total_poems + limit - 1) // limit

    return {
        "poems": poems,
        "total_pages": total_pages
    }


@router.get("/poems/{poem_id}")
async def get_poem(
    poem_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    poem = daos.poems_dao.get_poem_by_id(db, poem_id)
    if not poem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Poem not found")
    
    author = daos.get_user_by_id(db, poem.author_id)

    return {
        "id": poem.id,
        "title": poem.title,
        "content": poem.content,
        "author": {
            "id": author.id,
            "email": author.email,
            "name": author.name,
        }
    }
