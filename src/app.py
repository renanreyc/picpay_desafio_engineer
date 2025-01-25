import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from http import HTTPStatus

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from src.models import User
from src.schemas import Message, UserSchema, UserPublic, UserList
from src.database import get_session
from src.utils.password import hash_password, verify_password

app = FastAPI()

@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello, World!'}

@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):

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


    db_user = User(
        username=user.username, 
        password=hash_password(user.password), 
        email=user.email
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

@app.get('/users/', response_model = UserList)
def read_users(
        limit: int = 10,
        page: int = 0,
        session: Session = Depends(get_session)
    ):
    user = session.scalars(
            select(User).limit(limit).offset(page)
        )
    return {'users': user}

@app.get('/users/{user_id}', response_model=UserPublic)
def read_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(User.id == user_id)
    )
    if not db_user:
        raise HTTPException(
            status_code = HTTPStatus.NOT_FOUND, detail= 'User not found'
        )
    
    return db_user

@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(User.id == user_id)
    )
    if not db_user:
        raise HTTPException(
            status_code = HTTPStatus.NOT_FOUND, detail= 'User not found'
        )

    db_user.email = user.email
    db_user.username = user.username
    db_user.password = user.password

    session.commit()
    session.refresh(db_user)

    return db_user

@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(User.id == user_id)
    )
    if not db_user:
        raise HTTPException(
            status_code = HTTPStatus.NOT_FOUND, detail= 'User not found'
        )

    session.delete(db_user)
    session.commit()

    return {'message': 'User deleted!'}