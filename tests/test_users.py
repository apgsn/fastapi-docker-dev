import pytest
from app.schemas import Token
from app.oauth2 import verify_access_token


def test_login_user(test_user, client):
    res = client.post(
        '/login',
        data={
            'username': test_user['email'],
            'password': test_user['password'],
        }
    )
    assert res.status_code == 200
    token = res.json()
    Token(**token)
    assert verify_access_token(token['access_token']) == test_user['id']

@pytest.mark.parametrize('email, password, status_code', [
    ('test@gmail.com', 'test', 403),
    ('test@gmail.com', 'wrong pw', 403),
    ('wrongmail@gmail.com', 'test', 403),
    (None, 'test', 422),
    ('wrongmail@gmail.com', None, 422),
    ('test1234', None, 422),
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        '/login',
        data={
            'username': email,
            'password': password,
        }
    )

    assert res.status_code == status_code
    if status_code == 403:
        assert res.json().get('detail') == 'Invalid credentials'
