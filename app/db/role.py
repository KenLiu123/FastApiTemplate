from app.models.db_user import User_Roles, Role_Permissions, Roles, Permissions
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.db.user import get_user            
from functools import wraps
from app.models.db_user import User, User_Roles, Role_Permissions, Roles, Permissions

# 给用户分配角色
async def assign_role_to_user(db: AsyncSession, user_name: str, role_name: str)->User_Roles:
    user = await get_user(db, user_name)
    if user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    role = await get_role(db, role_name)
    if role is None:
        raise HTTPException(status_code=404, detail="角色不存在")
    user_role = User_Roles(user_id=user.user_id, role_id=role.role_id)
    db.add(user_role)
    await db.commit()
    await db.refresh(user_role)
    return user_role


# 给角色分配权限
async def assign_permission_to_role(db: AsyncSession, role_name: str, permission_name: str)->Role_Permissions:
    role = await get_role(db, role_name)
    if role is None:
        raise HTTPException(status_code=404, detail="角色不存在")
    permission = await get_permission(db, permission_name)
    if permission is None:
        raise HTTPException(status_code=404, detail="权限不存在")   
    role_permission = Role_Permissions(role_id=role.role_id, permission_id=permission.permission_id)
    db.add(role_permission)
    await db.commit()
    await db.refresh(role_permission)
    return role_permission

# 获取角色
async def get_role(db: AsyncSession, role_name: str) -> Optional[Roles]:
    result = await db.execute(select(Roles).filter(Roles.role_name == role_name))
    result = result.scalars()
    if result:
        return result.first()
    return None 

# 获取权限  
async def get_permission(db: AsyncSession, permission_name: str) -> Optional[Permissions]:
    result = await db.execute(select(Permissions).filter(Permissions.permission_name == permission_name))
    result = result.scalars()
    if result:
        return result.first()
    return None

# 获取用户角色
async def get_user_roles(db: AsyncSession, user_name: str) -> list[User_Roles]:
    user = await get_user(db, user_name)
    result = await db.execute(select(User_Roles).filter(User_Roles.user_id == user.user_id))
    result = result.scalars()
    return list(result) 

# 获取角色权限
async def get_role_permissions(db: AsyncSession, role_name: str) -> list[Role_Permissions]:
    role = await get_role(db, role_name)
    result = await db.execute(select(Role_Permissions).filter(Role_Permissions.role_id == role.role_id))
    result = result.scalars()
    return list(result) 

# 获取用户权限
async def get_user_permissions(db: AsyncSession, user_name: str) -> list[Permissions]:
    permissions = []
    user = await get_user(db, user_name)
    user_roles = await get_user_roles(db, user.username)
    for user_role in user_roles:
        role = await db.execute(select(Roles).filter(Roles.role_id == user_role.role_id))
        role = role.scalars().first()
        role_permissions = await get_role_permissions(db, role.role_name)
        for role_permission in role_permissions:
            permission = await db.execute(select(Permissions).filter(Permissions.permission_id == role_permission.permission_id))
            permission = permission.scalars().first()
            permissions.append(permission)
    print([permission.permission_name for permission in permissions])
    return permissions


def require_permission(permission_name: str):
    """装饰器：检查用户是否具有某个权限"""
    def decorator(func):
        @wraps(func)
        async def wrapper(user, db,  *args, **kwargs):
            result = await db.execute(select(User).filter(User.username == user.username))
            user = result.scalars().first()

            if not user:
                raise HTTPException(status_code=403, detail="无此用户")
            
            user_permissions = await get_user_permissions(db, user.username)  # 用户拥有的权限集合
            
            if permission_name not in [permission.permission_name for permission in user_permissions]:
                raise HTTPException(status_code=403, detail="无权限访问此接口")

            return await func(user=user, db=db,*args, **kwargs)
        return wrapper
    return decorator