from app import oauth2
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# Get all posts
@router.get("/", response_model= List[schemas.Post])

def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return posts

# Create new post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)

def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), 
                user_id: int = Depends(oauth2.get_current_user)):

    print(user_id)
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

# Get single post by ID

@router.get("/{id}", response_model= schemas.Post)

def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    return post

# Delete a post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)

def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    post.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update a post

@router.put("/{id}", response_model= schemas.Post)

def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    post.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post.first()
