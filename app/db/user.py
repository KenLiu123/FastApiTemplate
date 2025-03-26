# app/models/user.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.core.database import Base
from app.models.db_user import User



def get_user(db: AsyncSession, username: str) -> Optional[User]:
    user = db.execute(select(User).where(User.username == username)).scalar_one_or_none()
    return user


async def create_user(db: AsyncSession, user: User) -> User:
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    user = db.execute(select(User).where(User.email == email)).scalar_one_or_none()
    return user



    
