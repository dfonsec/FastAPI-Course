# Pydantic Schema
# We use the BaseModel class and pass it into the
# Schema class so it can inherit the BaseModel's attributes
from pydantic import BaseModel
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase):
    pass

