from fastapi import status, Depends, HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .schemas import TokenData
from .database import get_db
from .models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = 'sdkbfdjohgkgba3rhiwrfe,,h4r,ifbd o3ie'
ALGORITHM = 'HS256'
EXPIRATION_TIME = 60    # Minutes

def create_access_token(data: dict):
    payload = data.copy()
    expires = datetime.utcnow() + timedelta(minutes=EXPIRATION_TIME)
    payload.update({'exp': expires})

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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
