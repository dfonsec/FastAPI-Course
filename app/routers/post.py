from ..schemas import PostCreate, Post, PostBase
from ..models import Post
from ..database import get_db
from ..main import app
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, Response
from typing import List

@app.get("/posts", response_model=List[Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    
    #TODO: This might cause a bug between the Pydantic Post and the SQAlc model named Post as well, fix it ? 
    posts = db.query(Post).all()
    return posts


# body will extract all the fields from the body and
# then convert it into a python dictionary
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    
    # refresh takes the entry that was created in the db and updates the python object data to reflect what's in the db
    db.refresh(new_post)
    
    return new_post

# The ID field is a path parameter
@app.get("/posts/{id}", response_model=Post)
def get_post(id: int, db: Session = Depends(get_db)):
    
    # cursor.execute("""SELECT * FROM posts WHERE id= %s """, (str(id), ))
    # post = cursor.fetchone()
    post = db.query(Post).filter(Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found.")
            
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id= %s RETURNING *""", (str(id), ))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(Post).filter(Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found.")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", response_model=Post)
def update_post(id: int, post: PostBase,  db: Session = Depends(get_db)):
    # cursor.execute(f"""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    # Define query
    post_query = db.query(Post).filter(Post.id == id)
    
    # Grab post
    post_found = post_query.first()
    
    if not post_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')
    
    
    post_query.update(post.model_dump(), synchronize_session=False)
    
    db.commit()
    
    return post_query.first()