from fastapi import FastAPI
from .routers import post, user, auth, vote

# Creats table in db if it doesn't exist (obsolete, use alembic instead)
# Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(vote.router)
