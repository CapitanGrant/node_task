from fastapi import FastAPI
from app.tasks.router import router as task_router

app = FastAPI()


@app.get('/')
def home_page():
    return {"message": "Добро пожаловать! Данное приложение осуществляет "
                       "простое управление CRUD операциями по работе с задачами!"}


app.include_router(task_router)
