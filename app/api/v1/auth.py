from app.schemas.response import ResponseModel
from fastapi import APIRouter, Depends, HTTPException
from app.core.security import authenticate_user, create_access_token,verify_access_token, get_current_user
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.db.user import get_user_by_email, create_user, get_all_users as get_all_users_db, get_total_users
from app.schemas.user import UserCreate, UserLogin
from app.models.db_user import User as db_user
from app.db.role import require_permission
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
    

@app.get("/users/getallusers", response_model=ResponseModel)
@require_permission("manage_users")
async def get_all_users(page: int, page_size: int, user: db_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    users = await get_all_users_db(db, page=page, page_size=page_size)
    total = await get_total_users(db)
    json_users = []
    for user in users:
        json_users.append({
            "username": user.username,
            "email": user.email,
            "telephone": user.telephone,
            "avatar": user.avatar,
            "created_at": user.created_at,
            "is_active": user.is_active
        })
    return ResponseModel(status_code=200, status="success", message="Users fetched successfully", data={"users": json_users, "total": total})


