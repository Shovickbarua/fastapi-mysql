from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Union, Annotated
from . import model
from .database import SessionLocal, engine
from sqlalchemy.orm import Session

app = FastAPI()
model.Base.metadata.create_all(bind=engine)

class PostBase(BaseModel):
    title: str
    description: str
    user_id: int

class UserBase(BaseModel):
    name : str
    email : str

#Dependency
def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/users")
def get_users(db: db_dependency):
    users = db.query(model.User).all()
    return users

@app.post("/users")
def post_users(user: UserBase, db: db_dependency):
    user = model.User(**user.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get("/users/{id}")
def show_user(user_id: int, db: db_dependency):
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return user

@app.delete("/users/{id}")
def delete_user(id: int, db: db_dependency):
    user = db.query(model.Post).filter(model.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(user)
    db.commit()
    return user