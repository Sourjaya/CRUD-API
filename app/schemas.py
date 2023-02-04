from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic.types import conint

class PostBase(BaseModel):
    title:str
    content:str
    published: bool = True

class PostCreate(PostBase):
    pass

class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True
class Post(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    owner: User
    
    class Config:
        orm_mode = True
class PostOut(BaseModel):
    Post: Post
    votes: int

class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id:int
    dir: conint(ge=0,le=1)
