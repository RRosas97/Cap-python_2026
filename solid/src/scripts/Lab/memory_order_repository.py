from src.scripts.Lab.models.order import Order


class InMemoryOrderRepository:

    def __init__(self):
        self._orders: dict[int, Order] = {}
        self._siguiente_id = 1

    def add(self, order: Order) -> Order:
        order.id = self._siguiente_id
        self._orders[order.id] = order
        self._siguiente_id += 1
        return order

    def get(self, order_id: int) -> Order | None:
        return self._orders.get(order_id)

    def list_by_user(self, user_id: int) -> list[Order]:
        return [o for o in self._orders.values() if o.user_id == user_id]

    def update_status(self, order_id: int, status: str) -> Order | None:
        order = self._orders.get(order_id)
        if order is None:
            return None
        order.status = status
        return order

    def delete(self, order_id: int) -> bool:
        if order_id not in self._orders:
            return False
        del self._orders[order_id]
        return True
