from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..utils import verify
from ..oauth2 import create_access_token
from ..schemas import Token


router = APIRouter(
    tags=['Authentication'],
)

@router.post('/login', response_model=Token)
def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    print(credentials)
    user = db.query(User).filter(User.email == credentials.username).one_or_none()
    if not user or not verify(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid credentials'
        )         

    # Return JWT token
    return {
        'access_token': create_access_token(data = {'user_id': user.id}),
        'token_type': 'bearer',
    }
