from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, database, auth


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

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already used!",
        )

    return {
        'id': db_user.id,
        'email': user.email,
        'name': user.name,
    }


@app.post("/login")
def login(form_data: models.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.email).first()

    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

    access_token = auth.create_access_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "Bearer",
    }
