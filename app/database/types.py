import datetime
import typing
from typing import Optional

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship

if typing.TYPE_CHECKING:
    from app.ycomb import ytypes


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String(), primary_key=True)  # this is the username

    @staticmethod
    def from_ytype(user: "ytypes.User") -> "User":
        if user is None:
            return None
        return User(id=user.id)


class BaseObject:
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[Optional[str]] = mapped_column(ForeignKey("users.id"))

    @declared_attr
    def date(self):
        return mapped_column(DateTime, default=datetime.datetime.utcnow)

    @declared_attr
    def user(self):
        return relationship(User, foreign_keys=[self.user_id])


class Post(BaseObject, Base):
    __tablename__ = "posts"
    title: Mapped[str]
    text: Mapped[Optional[str]]
    comments: Mapped[Optional[typing.List["Comment"]]] = relationship(back_populates="post")

    @staticmethod
    def from_ytype(post: "ytypes.Post") -> "Post":
        return Post(
            id=post.id,
            date=post.date,
            # user_id=post.user.id,
            user=User.from_ytype(post.user),
            title=post.title,
            text=post.text,
        )


class Comment(BaseObject, Base):
    __tablename__ = "comments"
    text: Mapped[str]
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post: Mapped[Post] = relationship(back_populates="comments", foreign_keys=[post_id])

    @staticmethod
    def from_ytype(comment: "ytypes.Comment") -> "Comment":
        return Comment(
            id=comment.id,
            date=comment.date,
            user_id=comment.user.id,
            user=User.from_ytype(comment.user),
            text=comment.text,
            post_id=comment.post.id,
            post=Post.from_ytype(comment.post),
        )
