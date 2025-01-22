import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fastapi.testclient import TestClient

from src.models import table_registry
from src.app import app

@pytest.fixture()
def client():
    return  TestClient(app)

@pytest.fixture()
def session():
    engine = create_engine(
        'sqlite:///:memory:'
    )

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)