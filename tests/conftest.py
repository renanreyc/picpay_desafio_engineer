import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from contextlib import contextmanager
from datetime import datetime

import pytest
import factory
from fastapi.testclient import TestClient



from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool


from src.models import table_registry, User
from src.app import app
from src.database import get_session
from src.utils.password import hash_password

class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@1Pass')


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
    monkey_pass = 'Test@1234'
    user = UserFactory( password=hash_password(monkey_pass) )
    
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = monkey_pass

    return user

@pytest.fixture()
def user_two(session):
    user = UserFactory()
    
    session.add(user)
    session.commit()
    session.refresh(user)

    return user

@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data = {'username': user.email, 'password': user.clean_password}
    )

    return response.json()['access_token']