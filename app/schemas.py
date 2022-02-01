import datetime
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    created_at: datetime
    email: EmailStr

    class Config:
        orm_mode = True

class VoteSchema(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner: UserResponse
    votes: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str
