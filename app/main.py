from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from .routers import post, user, auth, vote

# from .database import engine
# from . import model

# model.Base.metadata.create_all(bind=engine) # alembic is use for db migrations

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"data": "root s"}


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(vote.router)
