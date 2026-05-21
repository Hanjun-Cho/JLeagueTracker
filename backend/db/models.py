from typing import Optional
from datetime import date
from sqlalchemy import ForeignKey, String, Integer, Date
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)

class Base(DeclarativeBase):
    pass

class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    JP_name: Mapped[str] = mapped_column(String)
    position: Mapped[str] = mapped_column(String)
    back_number: Mapped[str] = mapped_column(String)
    team: Mapped[str] = mapped_column(String)

    EN_name: Mapped[Optional[str]] = mapped_column(String, nullable=True) 
    transfermarkt_URL: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    date_of_birth: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    tasks = relationship("Task", back_populates="player")

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(String)
    task_type: Mapped[str] = mapped_column(String)
    player_id: Mapped[int] = mapped_column(Integer, ForeignKey("players.id"))

    player = relationship("Player", back_populates="tasks")
