from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)

    # "orders" no es una columna real -> es un atajo de Python para acceder
    # a todos los Order relacionados con este User, sin escribir un JOIN a mano.
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"User(id={self.id}, username={self.username!r})"
