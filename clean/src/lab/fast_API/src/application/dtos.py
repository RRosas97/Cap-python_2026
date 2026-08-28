from dataclasses import dataclass
from datetime import datetime


@dataclass
class OrderItemInputDTO:
    product_name: str
    quantity: int
    unit_price: float


@dataclass
class CreateOrderDTO:
    user_id: int
    items: list[OrderItemInputDTO]


@dataclass
class UpdateOrderStatusDTO:
    order_id: int
    status: str
    requesting_user_id: int


@dataclass
class OrderItemDTO:
    id: int
    product_name: str
    quantity: int
    unit_price: float
    subtotal: float


@dataclass
class OrderDTO:
    id: int
    user_id: int
    status: str
    created_at: datetime
    items: list[OrderItemDTO]
    total: float


@dataclass
class RegisterUserDTO:
    username: str
    email: str
    password: str


@dataclass
class LoginDTO:
    username: str
    password: str


@dataclass
class UserDTO:
    id: int
    username: str
    email: str


@dataclass
class TokenDTO:
    access_token: str
    token_type: str = "bearer"
