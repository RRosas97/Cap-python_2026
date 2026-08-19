from sqlalchemy import Boolean, Column, Integer, String

from src.models.base import Base


class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer(), primary_key=True)
    movie = Column(String(50), nullable=False, unique=True)
    name = Column(String(50), nullable=False)
    live = Column(Boolean(), default=True)

    def __str__(self):
        return self.name
