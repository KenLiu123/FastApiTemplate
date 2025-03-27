from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str  # 用于注册时传入的密码字段
    email: str

class UserLogin(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True  # 使得 Pydantic 模型可以从 SQLAlchemy ORM 模型自动转换


class TokenData(BaseModel):
    username: str   



