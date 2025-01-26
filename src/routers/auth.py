from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models import User
from src.schemas import Token
from src.database import get_session

from src.utils.password import verify_password
from src.utils.token import create_acess_token

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

T_Session = Annotated[Session, Depends(get_session)]
T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]

@router.post('/token', response_model=Token)
def login_for_acess_token(
    form_data: T_OAuth2Form,
    session: T_Session
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