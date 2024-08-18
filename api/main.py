from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app import models, database, auth
from daos import users_dao, poems_dao

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = users_dao.get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception
    return user

app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

@app.get("/")
async def liveness_probe():
    return {
        'title': 'FeenixAI API',
        'author': 'Mateus Oliveira',
        'date': '17/08/2024',
    }

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: models.UserCreate, db: Session = Depends(database.get_db)):
    hashed_password = auth.get_password_hash(user.password)
    db_user = users_dao.create_user(db, user, hashed_password)

    return {
        'id': db_user.id,
        'email': db_user.email,
        'name': db_user.name,
    }

@app.post("/login")
async def login(form_data: models.UserLogin, db: Session = Depends(database.get_db)):
    user = users_dao.get_user_by_email(db, form_data.email)

    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

    access_token = auth.create_access_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "Bearer",
    }

@app.post("/poems")
async def create_poem(
    poem: models.PoemCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    db_poem = poems_dao.create_poem(db, poem, current_user.id)
    return db_poem


@app.get("/poems")
async def get_poems(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return poems_dao.get_poems(db, skip, limit)


@app.put("/poems/{poem_id}")
async def update_poem(
    poem_id: int,
    poem: models.PoemCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    db_poem = poems_dao.get_poem_by_id(db, poem_id)
    if not db_poem or db_poem.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Poem not found or you do not have permission to edit this poem")

    updated_poem = poems_dao.update_poem(db, poem_id, poem.title, poem.content)
    return updated_poem
