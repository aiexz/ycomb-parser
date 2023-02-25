import datetime
from enum import Enum
from typing import Optional

import pydantic


class BaseModel(pydantic.BaseModel):
    class Config:
        orm_mode = True


class User(BaseModel):
    id: str


class BaseObject(BaseModel):
    id: int
    user: Optional[User]
    date: Optional[datetime.datetime]
    # these two are optional because they are not always present,
    # but we should make additional requests to get them and then
    # store them in the database and return them in the API


class Post(BaseObject):
    title: str  # always a link
    text: Optional[str]


class Comment(BaseObject):
    text: str
    post: Post


class YcombPages(Enum):
    NEW = "newest"
    PAST = "past"
    ASK = "ask"
    SHOW = "show"
    JOBS = "jobs"
    BEST = "best"
    ACTIVE = "active"
    NEWCOMMENTS = "newcomments"

    def __str__(self):
        return self.value
