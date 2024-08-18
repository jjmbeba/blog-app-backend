from fastapi import FastAPI, Depends

import crud.comment
import crud.favorite
import crud.post
import crud.tag
import crud.user
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import crud
import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def read_root():
    return {"Hello": "World"}

#User routes
@app.get('/users', response_model=list[schemas.UserWithAttributes])
def read_users(db:Session = Depends(get_db)):
    return crud.user.get_users(db)

@app.get('/users/{user_id}', response_model=schemas.UserWithAttributes)
def read_user(user_id:int, db:Session = Depends(get_db)):
    return crud.user.get_user(db, user_id)

@app.delete('/users/{user_id}')
def delete_user(user_id:int, db:Session = Depends(get_db)):
    return crud.user.delete_user(db, user_id)

@app.post('/users', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.user.create_user(db, user)

@app.get('/users/{user_id}/posts', response_model=list[schemas.PostWithAttributes])
def get_posts_for_user(user_id:int, db:Session = Depends(get_db)):
    return crud.user.get_posts_for_user(db, user_id)

#Post routes
@app.get('/posts')
def get_posts(db:Session = Depends(get_db)):
    return crud.post.get_posts(db)

@app.get('/posts/{post_id}')
def get_post(post_id:int, db:Session = Depends(get_db)):
    return crud.post.get_post(db, post_id)

@app.post('/users/{user_id}/posts', response_model=schemas.Post)
def create_post_for_user(user_id:int, post: schemas.PostCreate, db:Session = Depends(get_db)):
    return crud.post.create_post(db, post, user_id)

@app.delete('/posts/{post_id}')
def delete_post(post_id:int, db:Session = Depends(get_db)):
    return crud.post.delete_post(db, post_id)

@app.patch('/posts/{post_id}', response_model=schemas.Post)
def update_post(post_id:int, post: schemas.PostCreate, db:Session = Depends(get_db)):
    return crud.post.update_post(db, post_id, post)

#Tag routes
@app.get('/tags')
def get_tags(db:Session = Depends(get_db)):
    return crud.tag.get_tags(db)

@app.post('/tags')
def create_tag(tag: schemas.TagCreate, db:Session = Depends(get_db)):
    return crud.tag.create_tag(db, tag)

@app.delete('/tags/{tag_id}')
def delete_tag(tag_id:int, db:Session = Depends(get_db)):
    return crud.tag.delete_tag(db, tag_id)


#Comment routes
@app.post('/posts/{post_id}/comments', response_model=schemas.Comment)
def create_comment_for_post(post_id:int, comment: schemas.CommentCreate, db:Session = Depends(get_db)):
    return crud.comment.create_comment(db, comment, post_id)

@app.get('/posts/{post_id}/comments', response_model=list[schemas.CommentWithAttributes])
def read_post_comments(post_id:int, db:Session = Depends(get_db)):
    return crud.comment.get_post_comments(db, post_id)

#Favorite routes
@app.post('/favorites', response_model=schemas.Favorite)
def create_favorite(favorite: schemas.FavoriteCreate, db:Session = Depends(get_db)):
    return crud.favorite.create_favorite(db, favorite)

@app.get('/users/{user_id}/favorites', response_model=list[schemas.FavoriteWithAttributes])
def read_user_favorites(user_id:int, db:Session = Depends(get_db)):
    return crud.favorite.get_user_favorites(db, user_id)

@app.delete('/favorites/{favorite_id}')
def delete_user_favorite(favorite_id: int, db:Session = Depends(get_db)):
    return crud.favorite.delete_user_favorite(db, favorite_id)