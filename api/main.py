from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from src import models, database, auth


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
    db_user = models.User(email=user.email, name=user.name, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {
        'id': db_user.id,
        'email': user.email,
        'name': user.name,
    }
