from pwdlib import PasswordHash
import re

from http import HTTPStatus
from fastapi import HTTPException

pwd_context = PasswordHash.recommended()

def hash_password(password: str) -> str:
    _policy_password(password)
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def _policy_password(password: str):

    if len(password) < 8:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="A senha deve ter pelo menos 8 caracteres."
        )
    if not re.search(r'[A-Z]', password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="A senha deve conter pelo menos uma letra maiúscula."
        )
    if not re.search(r'[a-z]', password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="A senha deve conter pelo menos uma letra minúscula."
        )
    if not re.search(r'[0-9]', password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="A senha deve conter pelo menos um número."
        )
    if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="A senha deve conter pelo menos um caractere especial."
        )
    return True