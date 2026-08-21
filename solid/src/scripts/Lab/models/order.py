from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.scripts.Lab.models.base import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(20), nullable=False, default="pendiente")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")

    items = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )

    @property
    def total(self):
        return sum(item.subtotal for item in self.items)

    def __repr__(self):
        return f"Order(id={self.id}, status={self.status!r}, total={self.total})"
