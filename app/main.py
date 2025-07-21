from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import List
import pymysql
from pymysql.cursors import DictCursor
from . import models, schemas
import time

from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# -------------------- Routes --------------------

@app.get("/")

async def root():
    return {"message": "Hello, World!!!!!!"}

# Get all posts
@app.get("/posts", response_model= List[schemas.Post])

def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return posts

# Create new post

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)

def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

# Get single post by ID

@app.get("/posts/{id}", response_model= schemas.Post)

def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    return post

# Delete a post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)

def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    post.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update a post

@app.put("/posts/{id}", response_model= schemas.Post)

def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    post.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post.first()