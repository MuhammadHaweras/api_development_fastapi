from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
import pymysql
from pymysql.cursors import DictCursor
import time

app = FastAPI()

# -------------------- Database Connection --------------------

while True:
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="root",
            database="fastapi",
            cursorclass=DictCursor
        )
        cursor = conn.cursor()
        print("✅ Connected to MySQL")
        break
    except Exception as e:
        print("❌ Error connecting to DB:", e)
        time.sleep(3)

# -------------------- Pydantic Schema --------------------

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# -------------------- Helper Functions --------------------

def get_post_by_id(post_id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    return cursor.fetchone()

# -------------------- Routes --------------------

@app.get("/")
async def root():
    return {"message": "Hello, World!!!!!!"}

# Get all posts
@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    return cursor.fetchall()

# Create new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    cursor.execute(
        "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)",
        (new_post.title, new_post.content, new_post.published)
    )
    conn.commit()
    post_id = cursor.lastrowid
    return get_post_by_id(post_id)

# Get single post by ID
@app.get("/posts/{id}")
def get_post(id: int):
    post = get_post_by_id(id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    return post

# Delete a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = get_post_by_id(id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    cursor.execute("DELETE FROM posts WHERE id = %s", (id,))
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update a post
@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post):
    post = get_post_by_id(id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    cursor.execute(
        """
        UPDATE posts
        SET title = %s, content = %s, published = %s
        WHERE id = %s
        """,
        (updated_post.title, updated_post.content, updated_post.published, id)
    )
    conn.commit()
    return get_post_by_id(id)
