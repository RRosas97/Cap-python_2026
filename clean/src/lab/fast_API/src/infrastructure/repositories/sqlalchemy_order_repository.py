from lab.fast_API.src.domain.entities import Order, OrderItem
from lab.fast_API.src.infrastructure.db.models import OrderItemModel, OrderModel
from sqlalchemy.orm import Session


class SQLAlchemyOrderRepository:
    def __init__(self, session: Session):
        self._session = session

    def add(self, order: Order) -> Order:
        modelo = OrderModel(user_id=order.user_id, status=order.status)
        for item in order.items:
            modelo.items.append(
                OrderItemModel(
                    product_name=item.product_name,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                )
            )
        self._session.add(modelo)
        self._session.flush()

        return self._a_entidad(modelo)

    def get(self, order_id: int) -> Order | None:
        modelo = self._session.get(OrderModel, order_id)
        return self._a_entidad(modelo) if modelo else None

    def list_by_user(self, user_id: int) -> list[Order]:
        modelos = self._session.query(OrderModel).filter(OrderModel.user_id == user_id
                                                         ).all()
        return [self._a_entidad(m) for m in modelos]

    def update_status(self, order_id: int, status: str) -> Order | None:
        modelo = self._session.get(OrderModel, order_id)
        if modelo is None:
            return None
        modelo.status = status
        self._session.flush()
        return self._a_entidad(modelo)

    def delete(self, order_id: int) -> bool:
        modelo = self._session.get(OrderModel, order_id)
        if modelo is None:
            return False
        self._session.delete(modelo)
        self._session.flush()
        return True

    @staticmethod
    def _a_entidad(modelo: OrderModel) -> Order:
        items = [
            OrderItem(
                id=i.id,
                product_name=i.product_name,
                quantity=i.quantity,
                unit_price=i.unit_price,
            )
            for i in modelo.items
        ]
        return Order(
            id=modelo.id,
            user_id=modelo.user_id,
            items=items,
            status=modelo.status,
            created_at=modelo.created_at,
        )
