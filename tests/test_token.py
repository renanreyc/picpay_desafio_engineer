from http import HTTPStatus

import pytest
from jwt import decode
from fastapi.exceptions import HTTPException


from src.utils.token import create_acess_token, get_current_user
from src.settings import Settings

settings = Settings()

from http import HTTPStatus

def test_get_token(client, user):
    response = client.post(
        '/auth/token',
        data= { 'username': user.email,'password': user.clean_password }
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token

def test_token():
    data = { 'sub': 'test@test' }
    token = create_acess_token(data)
    
    result = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert result['sub'] == data['sub']
    

def test_exp_was_created():
    data = { 'sub': 'test@test' }
    token = create_acess_token(data)
    
    result = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    
    assert result['exp']

def test_get_current_user_with_error():
    with pytest.raises(HTTPException):
        get_current_user({})

def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
