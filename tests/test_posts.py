import pytest
from app.schemas import PostResponse

def test_get_posts(authorized_client, test_posts):
    res = authorized_client.get('/posts/')
    assert res.status_code == 200

    posts = res.json()
    assert len(posts) == len(test_posts)
    [PostResponse(**post) for post in posts]

def test_get_posts_unauthorized(client, test_posts):
    res = client.get('/posts/')
    assert res.status_code == 401

def test_get_post_unauthorized(client, test_posts):
    res = client.get(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401

def test_get_missing_post(authorized_client, test_posts):
    res = authorized_client.get('/posts/10000')
    assert res.status_code == 404

def test_get_post(authorized_client, test_posts):
    res = authorized_client.get(f'/posts/{test_posts[0].id}')
    assert res.status_code == 200
    PostResponse(**res.json())

@pytest.mark.parametrize('title, content, published', [
    ('elit', 'lorem ipsum', False),
    ('sit amet', 'lorem ipsumus', True),
    ('sit amet ⭐️', 'adipiscing elit', None),
])
def test_create_post(authorized_client, test_user, title, content, published):
    data = {
        'title': title,
        'content': content,
    }    
    if published is not None:
        data['published'] = published

    res = authorized_client.post('/posts/', json=data)
    assert res.status_code == 201
    post = res.json()
    PostResponse(**post)
    assert post['title'] == title
    assert post['content'] == content
    assert post['published'] == published if published else True
    assert post['owner']['id'] == test_user['id']

def test_create_post_unauthorized(client):
    res = client.post('/posts/', json={
        'title': 'title',
        'content': 'content',
    })
    assert res.status_code == 401

def test_delete_post_unauthorized(client, test_posts):
    res = client.delete(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401

def test_delete_post(authorized_client, test_posts):
    res = authorized_client.delete(f'/posts/{test_posts[0].id}')
    assert res.status_code == 204

def test_delete_missing_post(authorized_client, test_posts):
    res = authorized_client.delete('/posts/10000')
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_posts):
    res = authorized_client.delete(f'/posts/{test_posts[2].id}')
    assert res.status_code == 403

def test_update_post(authorized_client, test_posts):
    data = {
        'title': 'updated title',
        'content': 'updated content',
    }   
    res = authorized_client.put(f'/posts/{test_posts[0].id}', json=data)
    assert res.status_code == 200
    post = res.json()
    PostResponse(**post)    
    assert post['title'] == data['title']
    assert post['content'] == data['content']

def test_update_other_user_post(authorized_client, test_posts):
    data = {
        'title': 'updated title',
        'content': 'updated content',
    }   
    res = authorized_client.put(f'/posts/{test_posts[2].id}', json=data)
    assert res.status_code == 403

def test_update_post_unauthorized(client, test_posts):
    data = {
        'title': 'updated title',
        'content': 'updated content',
    }   
    res = client.put(f'/posts/{test_posts[0].id}', json=data)
    assert res.status_code == 401

def test_update_missing_post(authorized_client, test_posts):
    data = {
        'title': 'updated title',
        'content': 'updated content',
    }   
    res = authorized_client.put(f'/posts/10000', json=data)
    assert res.status_code == 404
