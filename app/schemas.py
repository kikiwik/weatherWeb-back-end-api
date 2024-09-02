# app/schemas.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    verification_code: str = None
class UserResponse(BaseModel):
    user_id: str
    email: str

    class Config:
        orm_mode = True

class UserLoginA(BaseModel):
    email: EmailStr
    password: str

class UserloginB(BaseModel)
    email: EmailStr
    verification_code: str = None
