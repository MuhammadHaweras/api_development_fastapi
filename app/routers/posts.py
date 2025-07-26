from app import oauth2
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi.responses import JSONResponse
from typing import List, Optional

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# Get all posts
@router.get("/")

def get_posts(
    db: Session = Depends(get_db),
    search: Optional[str] = "",
    limit: int = 10,
    skip: int = 0
):
    # Apply filter to both queries
    post_query = db.query(models.Post).filter(
        models.Post.title.contains(search)
    )

    results = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("votes")
    ).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).filter(
        models.Post.title.contains(search)
    ).group_by(models.Post.id).offset(skip).limit(limit).all()

    posts_with_votes = [
        {
            **post.__dict__,
            "votes": votes
        }
        for post, votes in results
    ]
    return posts_with_votes

# Create new post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)

def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):

    print(current_user)
    new_post = models.Post(user_id=current_user.id ,**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

# Get single post by ID

@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    result = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("votes")
    ).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).filter(
        models.Post.id == id
    ).group_by(models.Post.id).first()

    if not result:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    post, votes = result
    post_dict = post.__dict__.copy()
    post_dict["votes"] = votes
    return post_dict

# Delete a post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)

def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    
    if post.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update a post

@router.put("/{id}", response_model= schemas.Post)

def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    
    if post.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post.first()
