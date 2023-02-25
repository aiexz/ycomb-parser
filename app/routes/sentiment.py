import sqlalchemy.exc
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import ycomb
from app.database import Database, Comment

router = APIRouter()


@router.get("/{id}")
async def sentiment(id: int, db: AsyncSession = Depends(Database)):
    try:
        text: str = (await db.execute(select(Comment.text).where(Comment.id == id))).scalar_one()
    except sqlalchemy.exc.NoResultFound:
        return {"error": "comment not found"}
    return ycomb.TextClassifier.classify_sentiment(text)
