""" This module contains data models of the application. """

import datetime
from typing import List

import sqlalchemy as sa
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqids import Sqids

class Base(DeclarativeBase):
    pass

sqids = Sqids(min_length=5)

db = SQLAlchemy(model_class=Base)

users_answers_assoc = Table(
    "users_answers_assoc",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("answer_id", ForeignKey("answer.id"), primary_key=True),
)

poll_tag_assoc = Table(
    "poll_tag_assoc",
    Base.metadata,
    Column("poll_id", ForeignKey("poll.id"), primary_key=True),
    Column("tag_id", ForeignKey("poll_tag.id"), primary_key=True),
)


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    password: Mapped[str] = mapped_column(db.String(128), nullable=False)
    username: Mapped[str] = mapped_column(db.String(30), unique=True, nullable=False)
    join_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now()
    )
    polls: Mapped[List["Poll"]] = relationship(back_populates="author")
    voted_answers: Mapped[List["Answer"]] = relationship(
        secondary=users_answers_assoc, back_populates="users"
    )

    @property
    def voted_polls(self) -> list:
        """Returns a set of polls that the user has voted in"""
        return [answer.poll for answer in self.voted_answers]

    @property
    def number_of_polls_created(self) -> int:
        """Returns the number of polls that the user has created"""
        return len(self.polls)

    @property
    def number_of_votes(self) -> int:
        """Returns the number of votes made by the user"""
        return len(self.voted_answers)
    
    def did_vote(self, poll) -> bool:
        """Returns True if the user has voted in the poll, False otherwise"""
        return poll in self.voted_polls

class PollTag(db.Model):
    __tablename__ = "poll_tag"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(64), nullable=False)
    polls: Mapped[List["Poll"]] = relationship(secondary="poll_tag_assoc", back_populates="tags")


class Poll(db.Model):
    __tablename__ = "poll"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"))
    author: Mapped[User] = relationship(back_populates="polls")
    name: Mapped[str] = mapped_column(db.String(128))
    answers: Mapped[List["Answer"]] = relationship(
        back_populates="poll", order_by="Answer.order", cascade="all, delete-orphan"
    )
    is_unlisted: Mapped[bool] = mapped_column(db.Boolean, default=False)
    created: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now(), nullable=False
    )
    tags: Mapped[List["PollTag"]] = relationship(secondary="poll_tag_assoc", back_populates="polls")

    @property
    def total_number_of_votes(self) -> int:
        """Returns the total number of votes in the poll"""
        return sum(answer.number_of_votes for answer in self.answers)
    
    @property
    def graph_data(self) -> tuple:
        """Returns the poll data in a format that can be used by the chart.js library"""
        return tuple([(answer.text, answer.number_of_votes, answer.answer_percent) for answer in self.answers])
    
    @property
    def hashed_id(self) -> str:
        """Returns the hash of the poll id"""
        return sqids.encode([self.id])


class Answer(db.Model):
    __tablename__ = "answer"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    poll_id: Mapped[int] = mapped_column(sa.ForeignKey("poll.id"))
    text: Mapped[str] = mapped_column(db.String(128))
    users: Mapped[List["User"]] = relationship(
        secondary=users_answers_assoc, back_populates="voted_answers"
    )
    order: Mapped[int] = mapped_column(db.Integer)
    poll: Mapped[Poll] = relationship(back_populates="answers")

    @property
    def number_of_votes(self) -> int:
        """Returns the number of votes for the answer"""
        return len(self.users)

    @property
    def answer_percent(self) -> float:
        """Returns the percentage of votes for the answer"""
        total_votes = self.poll.total_number_of_votes
        if total_votes == 0:
            return 0
        return (self.number_of_votes / total_votes) * 100
