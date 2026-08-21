from src.scripts.Lab.models.order import Order
from src.scripts.Lab.order_repository import OrderRepository


class OrderService:
    """
    Depende del PUERTO (OrderRepository), no de ninguna implementación
    concreta. No sabe -- ni le importa -- si por dentro guarda en
    memoria, SQL Server, o cualquier otra cosa que cumpla el contrato.
    """

    def __init__(self, repository: OrderRepository):
        self._repository = repository

    def crear_orden(self, user_id: int, status: str = "pendiente") -> Order:
        orden = Order(user_id=user_id, status=status)
        return self._repository.add(orden)

    def obtener_orden(self, order_id: int) -> Order | None:
        return self._repository.get(order_id)

    def listar_ordenes_de_usuario(self, user_id: int) -> list[Order]:
        return self._repository.list_by_user(user_id)

    def marcar_como_pagada(self, order_id: int) -> Order | None:
        return self._repository.update_status(order_id, "pagado")

    def cancelar_orden(self, order_id: int) -> bool:
        return self._repository.delete(order_id)
