from http import HTTPStatus

from src.schemas import UserPublic

def test_read_root_return_ok(client):    
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK

def test_read_root_return_hello_world(client):   
    response = client.get('/')

    assert response.json() == {'message': 'Hello, World!'}

def test_create_user(client):
    response = client.post('/users/', 
                json={
        'username':'test',
        'email': 'test@test.com',
        'password': 'password'
    })

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username':'test',
        'email': 'test@test.com'
    }


def test_create_user_should_return_400_username_exists(
    client, user
):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}

def test_create_user_should_return_400_email_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': user.email,
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}

def test_delete_user_should_return_not_found(client):
    response = client.delete('/users/666')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user_should_return_not_found(client):
    response = client.put(
        '/users/666',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_get_user_should_return_not_found(client):
    response = client.get('/users/666')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}

def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == { 'users': [] }

def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get('/users/')
    
    assert response.status_code == HTTPStatus.OK
    assert response.json() == { 'users': [user_schema] }

def test_update_user(client, user):
    UserPublic.model_validate(user).model_dump()

    response = client.put(
        '/users/1',
        json={
            'id': 1,
            'username':'testput',
            'password': 'newpass',
            'email': 'test@test.com'
        }
    )

    assert response.json() == {
            'id': 1,
            'username':'testput',
            'email': 'test@test.com'
        }

def test_delete_user(client, user):
    UserPublic.model_validate(user).model_dump()
    
    response = client.delete('/users/1')

    assert response.json() == {'message': 'User deleted!'}

