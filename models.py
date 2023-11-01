from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, Column, Table
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
    password: Mapped[str] = mapped_column(db.String(128), nullable=False)
    username: Mapped[str] = mapped_column(db.String(30), unique=True, nullable=False)
    join_date: Mapped[datetime.date] = mapped_column(
        DateTime, default=datetime.date.today
    )
    polls: Mapped[List["Poll"]] = relationship(back_populates="author")
    voted_answers: Mapped[List["Answer"]] = relationship(
        secondary=users_answers_assoc, back_populates="users"
    )

    @property
    def voted_polls(self):
        return [answer.poll for answer in self.voted_answers]

    @property
    def number_of_polls_created(self):
        return len(self.polls)

    @property
    def number_of_votes(self):
        return len(self.voted_answers)


class Poll(db.Model):
    __tablename__ = "poll"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"))
    author: Mapped[User] = relationship(back_populates="polls")
    name: Mapped[str] = mapped_column(db.String(128))
    answers: Mapped[List["Answer"]] = relationship(
        back_populates="poll", order_by="Answer.order"
    )
    is_unlisted: Mapped[bool] = mapped_column(db.Boolean, default=False)

    @property
    def total_number_of_votes(self):
        return sum(answer.number_of_votes for answer in self.answers)


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
    def number_of_votes(self):
        return len(self.users)

    @property
    def answer_percent(self):
        total_votes = self.poll.total_number_of_votes
        if total_votes == 0:
            return 0
        return (self.number_of_votes / total_votes) * 100
