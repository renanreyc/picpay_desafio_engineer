from jwt import decode
from http import HTTPStatus
from src.utils.token import create_acess_token, SECRET_KEY, ALGORITHM

def test_token():
    data = { 'sub': 'test@test' }
    token = create_acess_token(data)
    
    result = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert result['sub'] == data['sub']
    

def test_exp_was_created():
    data = { 'sub': 'test@test' }
    token = create_acess_token(data)
    
    result = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    assert result['exp']

def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
