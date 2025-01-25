import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from http import HTTPStatus

from fastapi import FastAPI, HTTPException, Depends

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from src.models import User
from src.schemas import Message, UserSchema, UserPublic, UserList, Token
from src.database import get_session

from src.utils.password import hash_password, verify_password
from src.utils.token import create_acess_token, get_current_user

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
def update_user(
    user_id: int, 
    user: UserSchema, 
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    db_user = session.scalar(
        select(User).where(User.id == user_id)
    )
    if not db_user:
        raise HTTPException(
            status_code = HTTPStatus.NOT_FOUND, detail= 'User not found'
        )

    # to do: imp para current_user para o user alterar apenas seu próprio user.
    # if current_user.id != user_id:
    #     raise HTTPException(status_code=400, detail='Not enough permission')

    db_user.email = user.email
    db_user.username = user.username
    db_user.password = hash_password(user.password)

    session.commit()
    session.refresh(db_user)

    return db_user

@app.delete('/users/{user_id}', response_model=Message)
def delete_user(
    user_id: int, 
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    db_user = session.scalar(
        select(User).where(User.id == user_id)
    )
    if not db_user:
        raise HTTPException(
            status_code = HTTPStatus.NOT_FOUND, detail= 'User not found'
        )
    
    # to do: imp current_user para o user deletar apenas seu próprio user.
    # if current_user.id != user_id:
    #     raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Not enough permission')

    session.delete(db_user)
    session.commit()

    return {'message': 'User deleted!'}

@app.post('/auth/token', response_model=Token)
def login_for_acess_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    user = session.scalar(
        select(User).where(User.email == form_data.username)
    )

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=400, detail='Incorrect email or password'
        )
    
    access_token = create_acess_token(data_payload={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'Bearer'}