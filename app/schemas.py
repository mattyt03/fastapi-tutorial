from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


# the body of a post request will be validated & parsed using the template below
# the name and type of each field must match exactly
class PostBase(BaseModel):
    title: str
    content: str
    # published field is optional, defaults to true
    published: bool = True


class PostCreate(PostBase):
    pass


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

      
# this is a response model, it defines the fields we should send back to the user
# we may choose to omit certain fields in our response that are stored in the database
class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner: UserResponse
    # orm_mode will tell the Pydantic model to read the data even if it is not a dict, but an ORM model
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


# class TokenData(BaseModel):
#     id: Optional[str] = None