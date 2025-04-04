import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from app.core.config import settings
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.schemas.user import TokenData
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.db_user import User, User_Roles, Role_Permissions, Permissions, Roles
from functools import wraps
from fastapi import status
from app.core.database import AsyncSessionLocal

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# 用于密码哈希的上下文（bcrypt）
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 密钥（可以从环境变量中获取，但为了简单在此硬编码）
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# 用于生成和验证 JWT 的函数
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    生成访问令牌 (JWT)，并返回该令牌字符串。
    :param data: 存储在 token 中的用户数据（如用户ID、用户名等）。
    :param expires_delta: 令牌的过期时间，默认为 None，使用默认过期时间。
    :return: JWT 令牌
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 验证 JWT 是否有效
def verify_access_token(token: str) -> dict:
    """
    验证 JWT 令牌的有效性。
    :param token: JWT 令牌
    :return: JWT 中解码后的数据
    :raises: jwt.ExpiredSignatureError, jwt.JWTError
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.JWTError:
        raise Exception("Invalid token")

# 密码加密与验证函数
def get_password_hash(password: str) -> str:
    """
    将密码加密（哈希化）。
    :param password: 用户的密码
    :return: 哈希化后的密码
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码是否匹配（将输入密码与存储的哈希进行比较）。
    :param plain_password: 用户输入的密码
    :param hashed_password: 存储的哈希密码
    :return: 布尔值，表示密码是否匹配
    """
    return pwd_context.verify(plain_password, hashed_password)

async def authenticate_user(username: str, password: str, db: AsyncSession) -> Optional[User]:
    """
    验证用户名和密码是否匹配。
    :param username: 用户名
    :param password: 密码
    :param db: 数据库会话
    :return: 匹配的用户或 None  
    """ 
    user = await db.execute(select(User).where(User.username == username))
    user = user.scalar_one_or_none()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    """
    获取当前用户。
    :param db: 数据库会话
    :param token: OAuth2 令牌
    :return: 当前用户或 None
    """
    try:
        payload = verify_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except Exception as e:
        raise credentials_exception 
    
    user = await db.execute(select(User).where(User.username == token_data.username))
    user = user.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user 






