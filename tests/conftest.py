import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest

from fastapi.testclient import TestClient

from src.app import app

@pytest.fixture()
def client():
    return  TestClient(app)