from dataclasses import dataclass
from datetime import datetime, timezone

from lab.fast_API.src.domain.events import DomainEvent


@dataclass
class OrderItem:
    product_name: str
    quantity: int
    unit_price: float
    id: int | None = None

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        if self.unit_price <= 0:
            raise ValueError("El precio unitario debe ser mayor a 0")

    @property
    def subtotal(self) -> float:
        return self.quantity * self.unit_price


class Order:

    ESTADOS_VALIDOS = {"pendiente", "pagado", "cancelado", "enviado"}

    def __init__(
        self,
        user_id: int,
        items: list[OrderItem],
        id: int | None = None,
        status: str = "pendiente",
        created_at: datetime | None = None,
    ):
        if not items:
            raise ValueError("Una orden debe tener al menos un artículo")

        self.id = id
        self.user_id = user_id
        self.items = items
        self.status = status
        self.created_at = created_at or datetime.now(timezone.utc)
        self._events: list[DomainEvent] = []

    @staticmethod
    def create(user_id: int, items: list[OrderItem]) -> "Order":
        return Order(user_id=user_id, items=items)

    @property
    def total(self) -> float:
        return sum(item.subtotal for item in self.items)

    def change_status(self, nuevo_estado: str) -> None:
        if nuevo_estado not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido: {nuevo_estado}")
        self.status = nuevo_estado

    def add_event(self, event: DomainEvent) -> None:
        self._events.append(event)

    def pull_events(self) -> list[DomainEvent]:
        eventos = self._events[:]
        self._events.clear()
        return eventos

    def __repr__(self):
        return f"Order(id={self.id}, status={self.status!r}, total={self.total})"


@dataclass
class User:
    username: str
    email: str
    hashed_password: str
    id: int | None = None
