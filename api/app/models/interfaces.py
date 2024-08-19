from pydantic import BaseModel, EmailStr, constr
from typing import List


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: constr(min_length=6)

    class ConfigDict:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: constr(min_length=6)

    class ConfigDict:
        orm_mode = True


class PoemCreate(BaseModel):
    title: str
    content: str

    class ConfigDict:
        orm_mode = True


class CommentCreate(BaseModel):
    content: str

    class ConfigDict:
        orm_mode = True



class Author(BaseModel):
    id: int
    name: str
    email: str

    class ConfigDict:
        orm_mode = True


class CommentWithAuthor(BaseModel):
    id: int
    content: str
    author: Author

    class ConfigDict:
        orm_mode = True
