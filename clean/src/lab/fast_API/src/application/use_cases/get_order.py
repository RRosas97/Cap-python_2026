from lab.fast_API.src.application.dtos import OrderDTO, OrderItemDTO
from lab.fast_API.src.application.errors import ForbiddenError, NotFoundError
from lab.fast_API.src.domain.entities import Order
from lab.fast_API.src.domain.ports import UnitOfWorkPort


class GetOrderUseCase:
    def __init__(self, uow: UnitOfWorkPort):
        self._uow = uow

    def ejecutar(self, order_id: int, requesting_user_id: int) -> OrderDTO:
        with self._uow:
            orden = self._uow.orders.get(order_id)
            if orden is None:
                raise NotFoundError(f"Orden {order_id} no encontrada")
            if orden.user_id != requesting_user_id:
                raise ForbiddenError("No tienes permiso para acceder a esta orden")

            return self._to_dto(orden)

    @staticmethod
    def _to_dto(orden: Order) -> OrderDTO:
        return OrderDTO(
            id=orden.id,
            user_id=orden.user_id,
            status=orden.status,
            created_at=orden.created_at,
            items=[
                OrderItemDTO(
                    id=i.id, product_name=i.product_name, quantity=i.quantity,
                    unit_price=i.unit_price, subtotal=i.subtotal,
                )
                for i in orden.items
            ],
            total=orden.total,
        )
