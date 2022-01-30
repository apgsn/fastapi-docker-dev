from fastapi import FastAPI
from .models import Base
from .database import engine
from .routers import post, user, auth

# Creats table in db if it doesn't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
