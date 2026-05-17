from typing import Optional
from sqlalchemy import String, Integer
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
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

