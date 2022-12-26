from typing import List, Optional
from fastapi import Body, APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from .. import model, oauth2
from ..schemas import Post, PostCreate, PostOut


router = APIRouter(prefix="/posts", tags=["Post"])


@router.get("/", response_model=List[PostOut])
def get_posts(
    db: Session = Depends(get_db), limit: int = 10, skip: Optional[int] = None
):
    # posts = db.query(model.Post).limit(limit).offset(skip).all()
    posts = (
        db.query(model.Post, func.count(model.Vote.post_id).label("votes"))
        .join(model.Vote, model.Post.id == model.Vote.post_id, isouter=True)
        .group_by(model.Post.id)
        .limit(limit)
        .offset(skip)
        .all()
    )
    print(posts)
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_posts(
    post: PostCreate = Body(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(oauth2.get_current_user),
):
    # post.owner_id = user_id
    new_post = model.Post(**post.dict(), owner_id=user_id.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_posts(id: int, response: Response, db: Session = Depends(get_db)):
    post = db.query(model.Post).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    return {"data": post}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db)):
    post = db.query(model.Post).filter(model.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_posts(id: int, post: Post, db: Session = Depends(get_db)):
    post_query = db.query(model.Post).filter(model.Post.id == id)
    post_db = post_query.first()
    if post_db == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}
