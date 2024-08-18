from fastapi import FastAPI
from app import models, database, urls

app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

app.include_router(urls.router)

@app.get("/")
async def liveness_probe():
    return {
        'title': 'FeenixAI API',
        'author': 'Mateus Oliveira',
        'date': '17/08/2024',
    }
