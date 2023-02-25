from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession


class Database:
    async def __call__(self) -> AsyncGenerator[AsyncSession, None]:
        ...


class DatabaseMaker:
    def __init__(self, engine):
        self.engine = engine

    async def __call__(self):
        db = AsyncSession(self.engine)
        try:
            yield db
        finally:
            await db.close()
