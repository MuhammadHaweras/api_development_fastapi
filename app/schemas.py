from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    user_id: int
    created_at: datetime
    user: UserOut

    class Config:
        orm_mode = True

class PostOut(PostBase):
    Post: Post
    votes: int
    
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)

    class Config:
        orm_mode = True
