import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from http import HTTPStatus
from fastapi import FastAPI

from src.schemas import Message
from src.routers import users, auth

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)

@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello, World!'}