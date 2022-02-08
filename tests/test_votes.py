import pytest
from app.models import Vote

@pytest.fixture
def test_vote(test_posts, session, test_user):
    new_vote = Vote(post_id=test_posts[2].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()

def test_vote_unauthorized_user(client, test_posts):
    res = client.post(
        '/vote/',
        json={'post_id': test_posts[2].id, 'dir': 1},
    )
    assert res.status_code == 401

def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post(
        '/vote/',
        json={'post_id': test_posts[2].id, 'dir': 1},
    )
    assert res.status_code == 200

def test_vote_twice_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        '/vote/',
        json={'post_id': test_posts[2].id, 'dir': 1},
    )
    assert res.status_code == 409

def test_unlike(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        '/vote/',
        json={'post_id': test_posts[2].id, 'dir': 0},
    )
    assert res.status_code == 200

def test_unlike_missing(authorized_client, test_posts):
    res = authorized_client.post(
        '/vote/',
        json={'post_id': test_posts[2].id, 'dir': 0},
    )
    assert res.status_code == 409

def test_vote_missing_post(authorized_client, test_posts):
    res = authorized_client.post(
        '/vote/',
        json={'post_id': 10000, 'dir': 1},
    )
    assert res.status_code == 404
