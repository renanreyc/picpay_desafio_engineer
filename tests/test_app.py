import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from http import HTTPStatus
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_read_root_return_ok():    
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK

def test_read_root_return_hello_world():   
    response = client.get('/')

    assert response.json() == {'message': 'Hello, World!'}

    