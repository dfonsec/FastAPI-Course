from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite foods", "content": "I like pizza", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
    return None

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i
    return None
# This is a path operation
# The / is just the root path operatioj 
@app.get("/")
def main():
    return {"message": "Welcome to my "}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}


# body will extract all the fields from the body and
# then convert it into a python dictionary
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 10000000000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

# The ID field is a path parameter
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found.")
            
    return {"post_detail": post}


@app.delete("/posts/{id}")
def delete_post(id: int, status_code=status.HTTP_204_NO_CONTENT):
    post_idx = find_index_post(id)
    if not post_idx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')

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
    