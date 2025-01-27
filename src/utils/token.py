from datetime import datetime, timedelta, timezone
from http import HTTPStatus

from jwt import encode, decode, DecodeError
from jwt.exceptions import ExpiredSignatureError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models import User
from src.database import get_session
from src.settings import Settings

settings = Settings()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def create_access_token(data_payload: dict):
    to_encode = data_payload.copy()

    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    encoded_jwt = encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get('sub')
        if not email:
            raise credentials_exception
        # token_data = TokenData(username=username)
    except ExpiredSignatureError:
        raise credentials_exception
    except DecodeError:
        raise credentials_exception


    user_db = session.scalar(
        select(User).where(User.email == email)
    )

    if not user_db:
        raise credentials_exception
    
    return user_db

