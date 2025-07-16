from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")

async def root():
    return {"message": "Hello, World!!!!!!"}

@app.get("/posts")

def get_posts():
    return {"data": "This is your posts"}

@app.post("/createpost")

# def create_posts(payload: dict = Body(...)):
#     return {"message" : "success",
#             "title": f"{payload['title']}", 
#             "content": f"{payload['content']}"
#     }

def create_posts(new_post: Post):
    print(new_post.dict())
    return {
        "message": "success",
        "title" : new_post.title,
        "content" : new_post.content,
        "published": new_post.published,
        "rating": new_post.rating
    }