from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import schemas, models, oauth2
from app.database import get_db
from app import utils

router = APIRouter(
    tags=["Auth"]
)

@router.post("/login", response_model=schemas.Token)

def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # username is the email in OAuth2PasswordRequestForm
    db_user = db.query(models.User).filter(models.User.email == user.username).first()

    if not db_user or not utils.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    access_token = oauth2.create_access_token(data={"user_id": db_user.id})

    return {"access_token": access_token, "token_type": "bearer"}