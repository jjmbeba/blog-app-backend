from fastapi import HTTPException
from sqlalchemy.orm import Session
import models
import schemas

def create_comment(db:Session, comment: schemas.CommentCreate, post_id:int):
    db_comment = models.Comment(**comment.model_dump(), post_id=post_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    return db_comment

def get_post_comments(db:Session, post_id:int):
    return db.query(models.Comment).filter(models.Comment.post_id == post_id).all()

def delete_comment(db:Session, comment_id:int):
    db_comment = models.Comment.query(models.Comment).filter(models.Comment.id == comment_id).first()

    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    db.delete(db_comment)
    db.commit()

    return {}, 204