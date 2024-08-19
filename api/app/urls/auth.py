from app.config import database
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, daos, exceptions, auth


router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: models.UserCreate, db: Session = Depends(database.get_db)):
    hashed_password = auth.get_password_hash(user.password)
    try:
        db_user = daos.users_dao.create_user(db, user, hashed_password)
    except exceptions.UserEmailException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already used"
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    else:
        return {
            'id': db_user.id,
            'email': db_user.email,
            'name': db_user.name,
        }


@router.post("/login")
async def login(form_data: models.UserLogin, db: Session = Depends(database.get_db)):
    user = daos.users_dao.get_user_by_email(db, form_data.email)

    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

    access_token = auth.create_access_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
        }
    }
