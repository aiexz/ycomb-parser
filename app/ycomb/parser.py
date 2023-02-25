import asyncio
import datetime
from typing import AsyncGenerator

import aiohttp
import bs4
import sqlalchemy.exc

from app.database import Comment, DatabaseMaker
from app.ycomb import ytypes


async def get_page(page: str | ytypes.YcombPages) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://news.ycombinator.com/{page}") as response:
            return await response.text()


async def get_comments() -> AsyncGenerator[ytypes.Comment, None]:
    """
    Get last 30 from ycombinator
    :return: ``AsyncGenerator`` of ``ytypes.Comment``
    """
    page = await get_page(ytypes.YcombPages.NEWCOMMENTS)
    soup = bs4.BeautifulSoup(page, "html.parser")
    comments = soup.select(".athing")
    for comment in comments:
        id = comment.get("id")
        text = comment.select_one(".commtext")
        user = comment.select_one(".hnuser")
        date = comment.select_one(".age")
        python_date = datetime.datetime.strptime(date.get("title"), "%Y-%m-%dT%H:%M:%S")
        post_a = comment.select_one(".onstory").find("a")
        post = ytypes.Post(id=int(post_a.get("href")[8:]), title=post_a.text, text=None, user=None,
                           date=None)  # user and date should be received from the post in database
        yield ytypes.Comment(id=id, text=text.text, date=python_date, user=ytypes.User(id=user.text), post=post)


async def runner(db: DatabaseMaker):
    session = await anext(db())
    while True:
        async for x in get_comments():
            try:
                f = Comment.from_ytype(x)
                session.add(f)
                await session.commit()
            except sqlalchemy.exc.IntegrityError as e:
                await session.rollback()
        await asyncio.sleep(10)
