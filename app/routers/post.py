from typing import List, Optional
from fastapi import Response, status, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..models import Post
from ..schemas import PostBase, PostResponse
from ..utils import respond_404
from ..database import get_db
from ..oauth2 import get_current_user

router = APIRouter(
    prefix='/posts',    # Base route for all entrypoints
    tags=['Posts'],     # Tag for OpenAPI docs
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(
    post: PostBase,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    new_post = Post(owner_id=user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)    # Save newly created record into new_post, so it can be returned

    return new_post

@router.get('/', response_model=List[PostResponse])
def get_posts(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
    limit: Optional[int] = 10,
    offset: Optional[int] = None,
    search: Optional[str] = '',
):
    posts = db.query(Post) \
        .filter(or_(Post.title.contains(search), Post.content.contains(search))) \
        .limit(limit) \
        .offset(offset) \
        .all()
    return posts

@router.get('/{id}', response_model=PostResponse) # id is a path parameter
def get_post(
    id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == id).one_or_none()

    if not post:
        respond_404(id)

    return post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),    
):
    post_query = db.query(Post).filter(Post.id == id)
    deleted_post = post_query.one_or_none()

    if not deleted_post:
        respond_404(id)

    if deleted_post.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not authorized to perform this operation'
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=PostResponse)
def update_post(
    id: int,
    post: PostBase,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),        
):
    post_query = db.query(Post).filter(Post.id == id)
    updated_post = post_query.one_or_none()

    if not updated_post:
        respond_404(id)

    if updated_post.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not authorized to perform this operation'
        )

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(updated_post)

    return updated_post