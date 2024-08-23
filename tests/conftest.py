import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from madr.app import app
from madr.database import get_session
from madr.models import Book, Romancista, User, table_registry
from madr.security import get_password_hash, sanitize_string


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def client(session):
    def get_session_overrride():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_overrride
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def user(session):
    user_name = 'test_user'
    user_password = 'testtest'
    user_email = 'test_user@example.com'

    user = User(
        username=sanitize_string(user_name),
        email=user_email,
        password=get_password_hash(user_password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'testtest'  # monkeypatch

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    return response.json()['access_token']


@pytest.fixture
def book_1(session):
    book = Book(year=1973, title='café da manhã dos campeões', romancista_id=1)

    session.add(book)
    session.commit()
    session.refresh(book)

    return book


@pytest.fixture
def book_2(session):
    book = Book(year=1974, title='café da manhã dos campeões', romancista_id=1)

    session.add(book)
    session.commit()
    session.refresh(book)

    return book


@pytest.fixture
def romancista(session):
    romancista = Romancista(name=sanitize_string('Clarice Lispector'))

    session.add(romancista)
    session.commit()
    session.refresh(romancista)

    return romancista
