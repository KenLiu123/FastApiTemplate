from app.schemas.response import ResponseModel
from fastapi import APIRouter, Depends, HTTPException
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.role import require_permission




app = APIRouter()
@app.post("/item", response_model = ResponseModel)
async def add_posts()