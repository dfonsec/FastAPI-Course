# Pydantic Schema
# We use the BaseModel class and pass it into the
# Schema class so it can inherit the BaseModel's attributes
from pydantic import BaseModel
class Post(BaseModel):
    title: str
    content: str
    published: bool = True