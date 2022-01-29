import datetime
from pydantic import BaseModel

from app.database import Base
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostResponse(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
