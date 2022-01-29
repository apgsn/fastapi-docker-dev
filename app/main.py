from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .models import Base, Post
from .schemas import PostBase, PostResponse
from .database import get_db, engine

# Creats table in db if it doesn't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()


def respond_404(id: int):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Post with id {id} not found'
    )

@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostBase, db: Session = Depends(get_db)):
    new_post = Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)    # Save newly created record into new_post, so it can be returned

    return new_post

@app.get('/posts', response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts

@app.get('/posts/{id}', response_model=PostResponse) # id is a path parameter
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).one_or_none()

    if not post:
        respond_404(id)

    return post

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(Post).filter(Post.id == id)

    if not post_query.one_or_none():
        respond_404(id)

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}', response_model=PostResponse)
def update_post(id: int, post: PostBase, db: Session = Depends(get_db)):
    post_query = db.query(Post).filter(Post.id == id)
    updated_post = post_query.one_or_none()

    if not updated_post:
        respond_404(id)

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(updated_post)

    return updated_post
