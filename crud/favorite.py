from fastapi import HTTPException
from sqlalchemy.orm import Session
import models
import schemas

def create_favorite(db:Session, favorite: schemas.FavoriteCreate):
    db_favorite = models.Favorite(**favorite.model_dump())
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)

    return db_favorite

def get_user_favorites(db:Session, user_id:int):
    return db.query(models.Favorite).filter(models.Favorite.user_id == user_id).all()

def delete_user_favorite(db:Session, favorite_id:int):
    found_favorite = db.query(models.Favorite).filter(models.Favorite.id == favorite_id).first()

    if not found_favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    
    db.delete(found_favorite)
    db.commit()

    return {}, 204