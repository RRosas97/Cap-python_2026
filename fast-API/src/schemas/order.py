from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class OrderItemCreate(BaseModel):
    product_name: str = Field(min_length=1, max_length=100)
    quantity: int = Field(gt=0, description="Debe ser mayor a 0")
    unit_price: float = Field(gt=0, description="Debe ser mayor a 0")


class OrderItemOut(BaseModel):
    id: int
    product_name: str
    quantity: int
    unit_price: float
    subtotal: float

    model_config = {"from_attributes": True}


class OrderCreate(BaseModel):
    # al menos 1 artículo -> no tiene sentido una orden vacía
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderStatusUpdate(BaseModel):
    status: Literal["pendiente", "pagado", "cancelado", "enviado"]


class OrderOut(BaseModel):
    id: int
    user_id: int
    status: str
    created_at: datetime
    items: list[OrderItemOut]
    total: float

    model_config = {"from_attributes": True}
