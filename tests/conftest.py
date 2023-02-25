import asyncio
import datetime
import os
import random
import string

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine

from app.database import DatabaseMaker, Database, types


def text(length: int = 10) -> str:
    return "".join((random.choice(string.ascii_letters) for _ in range(length)))


async def get_db():
    if os.path.exists("test.db"):
        os.remove("test.db")
    engine = create_async_engine(os.getenv("YCOMB_DB", "sqlite+aiosqlite:///test.db"))
    db = DatabaseMaker(engine)
    async with engine.begin() as conn:
        await conn.run_sync(types.Base.metadata.create_all)
    session = await anext(db())
    users = [types.User(id=f"a{i}") for i in range(5)]
    session.add_all(users)
    posts = [types.Post(id=i, title=text(20), date=datetime.datetime.now(), user_id=random.choice(users).id, text=text(30))
             for i in range(3)]
    session.add_all(posts)
    comments = [types.Comment(id=i, text=text(30), date=datetime.datetime.now(), user_id=random.choice(users).id,
                              post=random.choice(posts)) for i in range(10)]
    comments[0].user = users[0]
    session.add_all(comments)
    await session.commit()
    return db


@pytest.fixture(scope='session')
def app():
    from app.main import app
    db = asyncio.run(get_db())
    app.dependency_overrides[Database] = db
    return TestClient(app)
