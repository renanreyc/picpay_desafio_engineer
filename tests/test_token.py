from http import HTTPStatus

from freezegun import freeze_time

import pytest
from jwt import decode
from fastapi.exceptions import HTTPException


from src.utils.token import create_access_token, get_current_user
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
    token = create_access_token(data)
    
    result = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert result['sub'] == data['sub']

def test_token_expired_after_time(client, user):
    with freeze_time('2024-01-26 09:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2024-01-26 09:31:00'):
        response = client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'wrongwrong',
                'email': 'wrong@wrong.com',
                'password': 'wrong',
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}

def test_refresh_token(client, token):
    response = client.post(
        '/auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert data['token_type'] == 'bearer'

def test_token_wrong_password(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': 'wrong_password'},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_exp_was_created():
    data = { 'sub': 'test@test' }
    token = create_access_token(data)
    
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
