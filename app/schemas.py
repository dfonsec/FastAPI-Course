# Pydantic Schema
# We use the BaseModel class and pass it into the
# Schema class so it can inherit the BaseModel's attributes
from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    
    
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    

