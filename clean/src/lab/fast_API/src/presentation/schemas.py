from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class OrderItemCreate(BaseModel):
    product_name: str = Field(min_length=1, max_length=100)
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)


class OrderCreateRequest(BaseModel):
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderStatusUpdateRequest(BaseModel):
    status: Literal["pendiente", "pagado", "cancelado", "enviado"]


class UserCreateRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)


# ---------- Responses (lo que el Presenter arma para el cliente) ----------

class OrderItemOut(BaseModel):
    id: int
    product_name: str
    quantity: int
    unit_price: float
    subtotal: float


class OrderOut(BaseModel):
    id: int
    user_id: int
    status: str
    created_at: datetime
    items: list[OrderItemOut]
    total: float


class UserOut(BaseModel):
    id: int
    username: str
    email: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
