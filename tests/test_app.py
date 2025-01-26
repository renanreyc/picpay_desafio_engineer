from http import HTTPStatus

def test_read_root_return_ok(client):    
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK

def test_read_root_return_hello_world(client):   
    response = client.get('/')

    assert response.json() == {'message': 'Hello, World!'}




