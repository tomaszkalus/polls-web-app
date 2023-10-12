from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, Column, Table, select, func
from sqlalchemy.ext.hybrid import hybrid_property
import datetime
from flask_login import UserMixin
import sqlalchemy as sa
from typing import List


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

users_answers_assoc = Table(
    "users_answers_assoc",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("answer_id", ForeignKey("answer.id"), primary_key=True),
)


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    email: Mapped[str] = mapped_column(db.String(254), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String(128), nullable=False)
    username: Mapped[str] = mapped_column(db.String(30), unique=True, nullable=False)
    join_date: Mapped[datetime.date] = mapped_column(DateTime, default=datetime.date.today)
    polls: Mapped[List["Poll"]] = relationship(backref="user")
    voted_answers: Mapped[List["Answer"]] = relationship(
        secondary=users_answers_assoc, back_populates="users"
    )
    @hybrid_property
    def number_of_polls_created(self):
        return len(self.polls)
    
    @number_of_polls_created.expression
    def number_of_polls_created(cls):
        return (
            select([func.count(Poll.id)])
            .where(Poll.user_id == cls.id)
            .label("number_of_polls_created")
        )
    
    @hybrid_property
    def number_of_votes(self):
        return len(self.voted_answers)
    
    @number_of_votes.expression
    def number_of_votes(cls):
        return (
            select([func.count(users_answers_assoc.c.user_id)])
            .where(users_answers_assoc.c.user_id == cls.id)
            .label("number_of_votes")
        )

class Poll(db.Model):
    __tablename__ = "poll"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"))
    name: Mapped[str] = mapped_column(db.String(128))
    answers: Mapped[List["Answer"]] = relationship(
        backref="poll", order_by="Answer.order"
    )
    expiration_datetime: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=True
    )


class Answer(db.Model):
    __tablename__ = "answer"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    poll_id: Mapped[int] = mapped_column(sa.ForeignKey("poll.id"))
    text: Mapped[str] = mapped_column(db.String(128))
    users: Mapped[List["User"]] = relationship(
        secondary=users_answers_assoc, back_populates="voted_answers"
    )
    order: Mapped[int] = mapped_column(db.Integer)

    @hybrid_property
    def number_of_votes(self):
        return len(self.users)

    @number_of_votes.expression
    def number_of_votes(cls):
        return (
            select([func.count(users_answers_assoc.c.user_id)])
            .where(users_answers_assoc.c.answer_id == cls.id)
            .label("number_of_votes")
        )
