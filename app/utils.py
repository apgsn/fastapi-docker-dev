from fastapi import status, HTTPException
from passlib.context import CryptContext


# Set bcrypt as hashing algorithm for passlib
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def respond_404(id: int):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Element with id {id} not found'
    )
