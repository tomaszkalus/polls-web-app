from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import DateTime
import datetime
from flask_login import UserMixin
import sqlalchemy as sa
from typing import List

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    email: Mapped[str] = mapped_column(db.String(254), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String(128), nullable=False)
    username: Mapped[str] = mapped_column(db.String(30), unique=True, nullable=False)
    polls: Mapped[List["Poll"]] = relationship(backref="user")


class Poll(db.Model):
    __tablename__ = "poll"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"))
    name: Mapped[str] = mapped_column(db.String(128))
    answers: Mapped[List["Answer"]] = relationship(backref="poll")
    expiration_datetime: Mapped[datetime.datetime] = mapped_column(DateTime)


class Answer(db.Model):
    __tablename__ = "answer"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    poll_id: Mapped[int] = mapped_column(sa.ForeignKey("poll.id"))
    text: Mapped[str] = mapped_column(db.String(128))
    votes: Mapped[int] = mapped_column(db.Integer)
