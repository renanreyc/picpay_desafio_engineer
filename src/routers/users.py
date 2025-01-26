from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from src.database import get_session
from src.schemas import Message, UserSchema, UserPublic, UserList
from src.models import User

from src.utils.password import hash_password
from src.utils.token import get_current_user


router = APIRouter(
    prefix='/users',
    tags=['users']
)

@router.get('/', response_model = UserList)
def read_users(
        limit: int = 10,
        page: int = 0,
        session: Session = Depends(get_session)
    ):
    user = session.scalars(
            select(User).limit(limit).offset(page)
        )
    return {'users': user}

@router.get('/{user_id}', response_model=UserPublic)
def read_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(User.id == user_id)
    )
    if not db_user:
        raise HTTPException(
            status_code = HTTPStatus.NOT_FOUND, detail= 'User not found'
        )
    
    return db_user

@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
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

@router.put('/{user_id}', response_model=UserPublic)
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
    #     raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Not enough permission')

    db_user.email = user.email
    db_user.username = user.username
    db_user.password = hash_password(user.password)

    session.commit()
    session.refresh(db_user)

    return db_user


@router.delete('/{user_id}', response_model=Message)
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
    #     raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Not enough permission')

    session.delete(db_user)
    session.commit()

    return {'message': 'User deleted!'}