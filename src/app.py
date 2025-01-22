import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, select, or_
from sqlalchemy.orm import Session

from src.models import User
from src.schemas import Message, UserSchema, UserPublic, UserDB, UserList
from src.settings import Settings

app = FastAPI()

database = []

@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello, World!'}

@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    engine = create_engine(Settings().DATABASE_URL)

    with Session(engine) as session:
        db_user = session.scalar(
            select(User).where(
                or_(User.username == user.username, User.email == user.email)
            )
        )

        if db_user:
            if db_user.username == user.username:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail='Username already exists'
                )
            elif db_user.email == user.email:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail='Email already exists'
                )
            
    db_user = User(username=user.username, email=user.email, password=user.password)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

@app.get('/users/', response_model = UserList)
def read_users():
    return {'users': database}

@app.get('/users/{user_id}', response_model=UserPublic)
def read_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code = HTTPStatus.NOT_FOUND, detail= 'User not found'
        )
    
    return database[user_id - 1]

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