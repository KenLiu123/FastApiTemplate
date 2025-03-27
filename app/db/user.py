# app/models/user.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.core.database import Base
from app.models.db_user import User as db_user
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_access_token
from fastapi import Depends
from app.core.database import get_db
from app.schemas.user import TokenData

async def get_user(db: AsyncSession, username: str) -> Optional[db_user]:
    result  = await db.execute(select(db_user).filter(db_user.username == username))
    result = result.scalars()
    if result:
        user = result.first()  
        if user:
            return user
    return None


async def create_user(db: AsyncSession, user: UserCreate) -> db_user:
    user = db_user(username=user.username, email=user.email, password=get_password_hash(user.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[db_user]:
    result = await db.execute(select(db_user).filter(db_user.email == email)) 
    result = result.scalars()
    if result:
        user = result.first()
        if user:
            return user
    return None




