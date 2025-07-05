from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time

app = FastAPI()

# Pydantic Schema
# We use the BaseModel class and pass it into the
# Schema class so it can inherit the BaseModel's attributes
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

while True: 
    try:
        conn = psycopg.connect(host='localhost', dbname='fastapi', 
                            user='postgres', password='postgres',
                            row_factory=dict_row)
        cursor = conn.cursor()
        print("Database connection was successful")
        break

    except Exception as error:
        print("Connecting to database failed")
        print("Error was:", error)
        time.sleep(2)
    

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite foods", "content": "I like pizza", "id": 2}]



# This is a path operation
# The / is just the root path operation
@app.get("/")
def main():
    return {"message": "Welcome to my "}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


# body will extract all the fields from the body and
# then convert it into a python dictionary
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    
    return {"data": new_post}

# The ID field is a path parameter
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    
    cursor.execute(f"""SELECT * FROM posts WHERE id={id}""")
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found.")
            
    return {"post_detail": post}


@app.delete("/posts/{id}")
def delete_post(id: int, status_code=status.HTTP_204_NO_CONTENT):
    cursor.execute(f"""DELETE FROM posts WHERE id={id}""")
    

    my_posts.pop(post_idx)
    # 204 you don't want to send any data back
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    post_idx = find_index_post(id)
    
    if not post_idx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')
    
    post_dict = post.model_dump()
    post_dict["id"] = id
    my_posts[post_idx] = post_dict
    
    return {"data": post_dict}
    