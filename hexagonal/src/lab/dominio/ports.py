from typing import Protocol

from dominio.entities import Order


class OrderRepository(Protocol):
    def guardar(self, order: Order) -> None: ...

    def obtener(self, order_id: str) -> Order | None: ...

    def listar_por_usuario(self, user_id: str) -> list[Order]: ...


class NotificationPort(Protocol):
    def notificar_orden_creada(self, order: Order) -> bool: ...
