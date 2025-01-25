import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from contextlib import contextmanager
from datetime import datetime

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from src.models import table_registry, User
from src.app import app
from src.database import get_session

@pytest.fixture()
def client(session):

    def get_session_override():
        return session
        ...
    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override

        yield client
    
    app.dependency_overrides.clear()

@pytest.fixture()
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass = StaticPool
    )

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)

@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):
    def fake_time_handler(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_handler)

    yield time

    event.remove(model, 'before_insert', fake_time_handler)

@pytest.fixture
def mock_db_time():
    return _mock_db_time

@pytest.fixture()
def user(session):
    user = User(username='test', email = 'test@test.com', password='test')
    
    session.add(user)
    session.commit()
    session.refresh(user)

    return user