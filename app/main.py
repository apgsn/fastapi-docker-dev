from random import random
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import random

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

posts_cache = [] 

@app.get('/')
def root():
    return {'message': 'Hello World'}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = random.randrange(1, 10000)
    posts_cache.append(post_dict)
    return {'data': post_dict}

@app.get('/posts')
def get_posts():
    return {'data': posts_cache}

def find_post(id: int):
    post = next((el for el in posts_cache if el['id'] == id), None)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )
    return post, posts_cache.index(post)

@app.get('/posts/{id}') # id is a path parameter
def get_post(id: int, response: Response):
    post, _ = find_post(id)
    return {'data': post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post, _ = find_post(id)
    posts_cache.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    new_post = post.dict()
    _, index = find_post(id)
    new_post['id'] = id
    posts_cache[index] = new_post
    return {'data': new_post}
