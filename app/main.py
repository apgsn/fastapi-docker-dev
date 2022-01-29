from random import random
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import os
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

while True:
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_DATABASE'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print('Database connection established')
        break
    except Exception as e:
        print(f'Database connection error: {e}')
        time.sleep(5)


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(
        'INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *',
        (post.title, post.content, post.published)
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {'data': new_post}

@app.get('/posts')
def get_posts():
    cursor.execute('SELECT * FROM posts')
    posts = cursor.fetchall()
    return {'data': posts}

def find_post(id):
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post with id {id} not found'
        )
    return post

@app.get('/posts/{id}') # id is a path parameter
def get_post(id: int, response: Response):
    cursor.execute('SELECT * FROM posts WHERE id=%s', (id,))
    post = find_post(id)
    return {'data': post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(
        'DELETE FROM posts WHERE id=%s RETURNING *',
        (id,)
    )
    find_post(id)
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    cursor.execute(
        'UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *',
        (post.title, post.content, post.published, id)
    )
    updated_post = find_post(id)
    conn.commit()
    return {'data': updated_post}
