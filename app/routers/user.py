from fastapi import status, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from ..models import User
from ..schemas import UserCreate, UserResponse
from ..database import get_db
from ..utils import hash, respond_404

router = APIRouter(
    prefix='/users',
    tags=['Users'],
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check that mail has not been taken
    found_user = db.query(User).filter(User.email == user.email).one_or_none()
    if found_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Cannot create user with these credentials'
        )

    # Hash pwd
    user.password = hash(user.password)

    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/{id}', response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).one_or_none()
    if not user:
        respond_404(id)
    
    return user
