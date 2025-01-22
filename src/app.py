import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, HTTPException
from http import HTTPStatus

from src.schemas import Message, UserSchema, UserPublic, UserDB, UserList

app = FastAPI()

database = []

@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello, World!'}

@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):

    user_with_id = UserDB(
        id=len(database) + 1, **user.model_dump()
    )
    
    database.append(user_with_id)

    return user_with_id

@app.get('/users/', response_model = UserList)
def read_users():
    return {'users': database}

@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code = HTTPStatus.NOT_FOUND, detail= 'User not found'
        )


    user_with_id = UserDB(id=user_id, **user.model_dump())

    database[ user_id - 1 ] = user_with_id

    return user_with_id

@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code = HTTPStatus.NOT_FOUND, detail= 'User not found'
        )

    del database[user_id - 1]

    return {'message': 'User deleted!'}