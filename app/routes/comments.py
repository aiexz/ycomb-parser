from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.database.database import Database
from app.database.types import Comment
from app.ycomb import ytypes

router = APIRouter()


@router.get("/", response_model=List[ytypes.Comment])
async def comments(limit: int = 30, db: AsyncSession = Depends(Database)):
    res = (await db.execute(
        select(Comment).options(joinedload(Comment.post), joinedload(Comment.user)).order_by(Comment.date.desc()).limit(
            limit))).scalars()
    return (ytypes.Comment.from_orm(c) for c in res)


@router.get("/user/{id}", response_model=List[ytypes.Comment])
async def comments_by_user(id: str, limit: int = 30, db: AsyncSession = Depends(Database)):
    res = (await db.execute(select(Comment).options(joinedload(Comment.post), joinedload(Comment.user)).where(
        Comment.user_id == id).order_by(Comment.date.desc()).limit(limit))).scalars()
    return (ytypes.Comment.from_orm(c) for c in res)
