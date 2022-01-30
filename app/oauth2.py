import os
from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.config import Settings
from .schemas import TokenData
from .database import get_db
from .models import User
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict):
    payload = data.copy()
    expires = datetime.utcnow() + timedelta(minutes=settings.jwt_expiration_time)
    payload.update({'exp': expires})

    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        user_id: str = payload.get('user_id')
        TokenData(id=user_id)    # Validate schema
    except JWTError:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    return user_id

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    token_id = verify_access_token(token)
    return db.query(User).filter(User.id == token_id).one_or_none()
