from fastapi import HTTPException
from sqlalchemy.orm import Session
import models
import schemas

def create_post(db:Session, post: schemas.PostCreate, user_id:int):
    db_post = models.Post(**post.model_dump(), user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post

def get_posts(db:Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()

def get_post(db:Session, post_id: int):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return db_post

def delete_post(db:Session, post_id: int):
    db_post = get_post(db, post_id)

    db.delete(db_post)
    db.commit()

    return {}, 204

def update_post(db:Session, post_id:int, post: schemas.PostCreate):
    found_post = get_post(db, post_id)

    for key, value in post.model_dump().items():
        setattr(found_post, key, value)

    db.commit()
    db.refresh(found_post)
    
    return found_post