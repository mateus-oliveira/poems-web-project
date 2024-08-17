from pydantic import BaseModel, EmailStr, constr


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: constr(min_length=6)

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: constr(min_length=6)

    class Config:
        orm_mode = True
