from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def liveness_probe():
    return {
        'project': 'FeenixAI API',
        'author': 'Mateus Oliveira',
        'date': '17/08/2024',
    }
