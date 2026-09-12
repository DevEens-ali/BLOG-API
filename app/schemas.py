from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    
class CategoryCreate(BaseModel):
    name: str

class CategoryResponse(BaseModel):
    id: int
    name: str

class PostCreate(BaseModel):
    title: str
    content: str
    author_id: int
    category_id: int

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    category_id: int
    created_at: datetime
    updated_at: datetime
    
class PostUpdate(BaseModel):
    title: str
    content: str
    category_id: int
    
class CommentCreate(BaseModel):
    content: str
    author_id: int
    post_id: int

class CommentResponse(BaseModel):
    id: int
    content: str
    author_id: int
    post_id: int
    created_at: datetime
    updated_at: datetime