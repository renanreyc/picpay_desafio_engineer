from http import HTTPStatus

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
        'password': 'password',
        'email': 'test@test.com'
    })

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username':'test',
        'email': 'test@test.com'
    }

def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == { 'users': [
        {
            'id': 1,
            'username':'test',
            'email': 'test@test.com'
        }
    ]}

def test_update_user(client):
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

def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.json() == {'message': 'User deleted!'}

