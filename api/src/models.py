from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, EmailStr, constr

Base = declarative_base()


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: constr(min_length=6)

    class Config:
        orm_mode = True


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    password = Column(String)
