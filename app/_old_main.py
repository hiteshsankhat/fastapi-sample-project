from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends

# import psycopg2
# from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from .database import engine, get_db
from . import model
from .schemas import Post

model.Base.metadata.create_all(bind=engine)

app = FastAPI()


my_posts = [
    {"title": "title1", "content": "content2", "id": 1},
    {"title": "title1", "content": "content2", "id": 2},
]

# try:
#     conn = psycopg2.connect(
#         host="192.168.0.111",
#         database="fastapi",
#         user="postgres",
#         password="password",
#         cursor_factory=RealDictCursor,
#     )
#     cursor = conn.cursor()
#     print("Data base connected")

# except Exception as error:
#     print("Error", error)


def find_post(id: int):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id: int):
    for idx, p in enumerate(my_posts):
        if p["id"] == id:
            return idx


@app.get("/")
def root():
    return {"data": "root"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(model.Post).all()
    return {"data": posts}
    # cursor.execute(""" SELECT * from posts """)
    # posts = cursor.fetchall()
    # return posts


@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def get_posts(id: int, response: Response, db: Session = Depends(get_db)):
    # post = find_post(id)
    post = db.query(model.Post).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': 'not found'}
    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post = Body(...), db: Session = Depends(get_db)):
    # new_post = {**post.dict(), "id": len(my_posts) + 1}
    # my_posts.append(new_post)

    # cursor.execute(
    #     """ Insert into posts (title, content, published) values (%s, %s, %s) RETURNING *;""",
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = model.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db)):
    post = db.query(model.Post).filter(model.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    # my_posts.pop(index)
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_posts(id: int, post: Post, db: Session = Depends(get_db)):
    post_query = db.query(model.Post).filter(model.Post.id == id)
    post_db = post_query.first()
    if post_db == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}
