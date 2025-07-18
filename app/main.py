from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [
    {"id": 1, "title": "Title of post 1", "content": "Content of post 1", "published": True},
    {"id": 2, "title": "Title of post 1", "content": "Content of post 1", "published": True}
  ]

def get_single_post(id):
    for p in my_posts:
        if p["id"] == id :
            return p

@app.get("/")

async def root():
    return {"message": "Hello, World!!!!!!"}

# get all posts
@app.get("/posts")

def get_posts():
    return my_posts

@app.post("/posts", status_code=status.HTTP_201_CREATED)

# creare a post
def create_posts(new_post: Post):
    post = new_post.dict()
    post["id"] = randrange(1, 1000000)
    my_posts.append(post)
    return post

#get post

@app.get("/posts/{id}")

def get_post(id: int):
   post = get_single_post(id)
   if not post:
       raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} not found")
   return post

# Delete Request

@app.delete("/posts/{id}",status_code= status.HTTP_204_NO_CONTENT)

def delete_post(id: int):
    idx = 0
    for p in my_posts:
        if p["id"] == id:
            idx = p["id"]
    
    my_posts.pop(idx)
    if not idx:
         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} not found")

    return Response(status_code= status.HTTP_204_NO_CONTENT)

#update
@app.put("/posts/{id}")

def update_post(id: int, post: Post):
     post_1 = get_single_post(id)
     if not post_1:
       raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} not found")
     updated_post= post.dict()
     post_1["title"] = updated_post['title']
     post_1["content"] = updated_post['content']
     return post_1
    