from dataclasses import dataclass


@dataclass
class CreateOrderDTO:
    user_id: str
    monto: float


@dataclass
class OrderDTO:
    id: str
    user_id: str
    monto: float
    estado: str
