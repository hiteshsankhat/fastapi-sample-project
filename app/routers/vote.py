from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from .. import model, schemas, database, oauth2

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(database.get_db),
    user_id: schemas.TokenData = Depends(oauth2.get_current_user),
):
    vote_query = db.query(model.Vote).filter(
        model.Vote.post_id == vote.post_id, model.Vote.user_id == user_id.id
    )
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Already voted"
            )
        new_vote = model.Vote(post_id=vote.post_id, user_id=user_id.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    if not found_vote:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="vote not exists"
        )
    vote_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "successfully deleted vote"}
