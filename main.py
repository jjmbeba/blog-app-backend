from fastapi import FastAPI, Depends

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
@app.get('/users', response_model=list[schemas.User])
def read_users(db:Session = Depends(get_db)):
    return crud.user.get_users(db)

@app.get('/users/{user_id}', response_model=schemas.User)
def read_user(user_id:int, db:Session = Depends(get_db)):
    return crud.user.get_user(db, user_id)

@app.delete('/users/{user_id}')
def delete_user(user_id:int, db:Session = Depends(get_db)):
    return crud.user.delete_user(db, user_id)

@app.post('/users', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.user.create_user(db, user)

#Post routes