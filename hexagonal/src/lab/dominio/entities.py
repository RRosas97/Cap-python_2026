import uuid
from dataclasses import dataclass


@dataclass
class Order:

    id: str
    user_id: str
    monto: float
    estado: str = "creada"

    @staticmethod
    def crear(user_id: str, monto: float) -> "Order":
        if not user_id.strip():
            raise ValueError("user_id no puede estar vacío")
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")
        return Order(id=str(uuid.uuid4()), user_id=user_id, monto=monto)
