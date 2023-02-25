import asyncio
import os

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine

from app import routes, ycomb
from app.database import Database, DatabaseMaker
from app.ycomb.parser import runner as parser_runner

app = FastAPI()

app.include_router(routes.comments, prefix="/comments", tags=["comments"])
app.include_router(routes.sentiment, prefix="/sentiment", tags=["sentiment"])


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.on_event("startup")
async def startup_event():
    if os.getenv("YCOMB_ML", "0").lower() in ("true", "1"):
        ycomb.TextClassifier.load_model()
    engine = create_async_engine(os.getenv("YCOMB_DB", "sqlite+aiosqlite:///ycomb.db"))
    db = DatabaseMaker(engine)
    app.dependency_overrides[Database] = db
    asyncio.create_task(parser_runner(db))
