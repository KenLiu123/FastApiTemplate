from app.schemas.response import ResponseModel
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import authenticate_user, create_access_token,verify_access_token, get_current_user
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.db.user import get_user_by_email, create_user
from fastapi import FastAPI
from app.schemas.user import UserCreate, UserLogin
from fastapi import Depends
from app.models.db_user import User as db_user
app = APIRouter()


@app.get("/", response_model=ResponseModel)
async def hello():
    return ResponseModel(status_code=200, status="success", message="Welcome to the API")


# 登录
@app.post("/users/login", response_model=ResponseModel)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(user.username, user.password, db)
    if not user:
        return ResponseModel(status_code=401, status="error", message="Invalid username or password")
    access_token = create_access_token(data={"sub": user.username})
    return ResponseModel(status_code=200, status="success", message="Login successful", data={"access_token": access_token, "token_type": "bearer"})

# 注册
@app.post("/users/register", response_model=ResponseModel)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email(db, user.email)
    if db_user:
        return ResponseModel(status_code=400, status="error", message="Email already registered")
    db_user = await create_user(db, user)
    return ResponseModel(status_code=200, status="success", message="User registered successfully", data={"user_id": db_user.user_id})    

# 登出
@app.post("/users/logout", response_model=ResponseModel)
async def logout(current_user: Annotated[db_user, Depends(get_current_user)]):
    if current_user:
        return ResponseModel(status_code=200, status="success", message="Logout successful")
    else:
        return ResponseModel(status_code=401, status="error", message="Unauthorized")
    




