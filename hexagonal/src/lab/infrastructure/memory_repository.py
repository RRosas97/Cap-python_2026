from dominio.entities import Order


class InMemoryOrderRepository:
    def __init__(self):
        self._ordenes: dict[str, Order] = {}

    def guardar(self, order: Order) -> None:
        self._ordenes[order.id] = order

    def obtener(self, order_id: str) -> Order | None:
        return self._ordenes.get(order_id)

    def listar_por_usuario(self, user_id: str) -> list[Order]:
        return [o for o in self._ordenes.values() if o.user_id == user_id]
