from fastapi import status, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from ..models import Post, Vote
from ..schemas import VoteSchema
from ..database import get_db
from ..utils import respond_404
from ..oauth2 import get_current_user

router = APIRouter(
    prefix='/vote',
    tags=['Vote'],
)


@router.post('/')
def vote(
    vote: VoteSchema,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == vote.post_id).one_or_none()
    if not post:
        respond_404(vote.post_id)
    
    found_vote = db.query(Vote) \
        .filter(Vote.post_id == vote.post_id, Vote.user_id == user.id) \
        .one_or_none()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {user.id} has already voted on post {vote.post_id}",
            )
        new_vote = Vote(post_id=vote.post_id, user_id=user.id)
        db.add(new_vote)
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {user.id} has not already voted on post {vote.post_id}",
            )
        db.delete(found_vote)

    db.commit()
    return {'success': True}
