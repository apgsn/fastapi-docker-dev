# Special pytest file, akl fixtures defined here
# will be accessible anywhere within the test folder.

import pytest
from app.schemas import UserResponse

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, get_db
from app.config import settings
from app.oauth2 import create_access_token
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Post

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}-test'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    data = {
        "email": "test@mailinator.com",
        "password": "test",
    }
    res = client.post('/users/', json=data)
    assert res.status_code == 201
    assert UserResponse(**res.json())

    # Create extra user
    client.post('/users/', json={
        "email": "test2@mailinator.com",
        "password": "test2",
    })

    return {
        **res.json(),
        'password': data["password"],
    }

@pytest.fixture
def token(test_user):
    return create_access_token({'user_id': test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session):
    posts = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id'],
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id'],
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": 2,
    }]

    session.add_all([Post(**post) for post in posts])
    session.commit()
    return session.query(Post).all()
