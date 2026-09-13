from pydantic import BaseModel, EmailStr, field_validator
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

    @field_validator("title", "content")
    @classmethod
    def sanitize_text(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Field cannot be empty")

        return value

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

    @field_validator("title", "content")
    @classmethod
    def sanitize_text(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Field cannot be empty")

        return value
    
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