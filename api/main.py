from fastapi import FastAPI

from app import models, urls
from app.config import database
from app.config.cors import cors


app = FastAPI()
app.add_middleware(**cors)

models.Base.metadata.create_all(bind=database.engine)

app.include_router(urls.router)

@app.get("/")
async def liveness_probe():
    return {
        'title': 'FeenixAI API',
        'author': 'Mateus Oliveira',
        'date': '17/08/2024',
    }
