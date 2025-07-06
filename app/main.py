from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg
from psycopg.rows import dict_row
from . import models, schemas
from .database import engine, SessionLocal, get_db
import time
from sqlalchemy.orm import Session
from .schemas import PostBase, PostCreate

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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

# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data": posts}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}


# body will extract all the fields from the body and
# then convert it into a python dictionary
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return {"data": new_post}

# The ID field is a path parameter
@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    
    # cursor.execute("""SELECT * FROM posts WHERE id= %s """, (str(id), ))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found.")
            
    return {"post_detail": post}


@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db), status_code=status.HTTP_204_NO_CONTENT):
    # cursor.execute("""DELETE FROM posts WHERE id= %s RETURNING *""", (str(id), ))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found.")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: PostBase,  db: Session = Depends(get_db)):
    # cursor.execute(f"""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    # Define quert 
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    # Grab post
    post_found = post_query.first()
    
    if not post_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')
    
    
    post_query.update(post.model_dump(), synchronize_session=False)
    
    db.commit()
    
    return {"data": post_query.first()}
    