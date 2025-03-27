from sqlalchemy import Column, Integer, String, TIMESTAMP, func, ForeignKey,Boolean
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    is_active = Column(Boolean, default=True)
    telephone = Column(String(11), nullable=False)
    avatar = Column(String(255))


class User_Roles(Base):
    __tablename__ = "user_roles"

    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.role_id"), primary_key=True)
    assigned_at = Column(TIMESTAMP, server_default=func.current_timestamp())

class Roles(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))


class Permissions(Base):
    __tablename__ = "permissions"

    permission_id = Column(Integer, primary_key=True, autoincrement=True)
    permission_name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))

class Role_Permissions(Base):
    __tablename__ = "role_permissions"

    role_id = Column(Integer, ForeignKey("roles.role_id"), primary_key=True)
    permission_id = Column(Integer, ForeignKey("permissions.permission_id"), primary_key=True)
    granted_at = Column(TIMESTAMP, server_default=func.current_timestamp())

