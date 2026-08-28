from lab.fast_API.src.application.dtos import OrderDTO, OrderItemDTO
from lab.fast_API.src.domain.entities import Order
from lab.fast_API.src.domain.ports import UnitOfWorkPort


class ListOrdersUseCase:
    def __init__(self, uow: UnitOfWorkPort):
        self._uow = uow

    def ejecutar(self, user_id: int) -> list[OrderDTO]:
        with self._uow:
            ordenes = self._uow.orders.list_by_user(user_id)
            return [self._to_dto(o) for o in ordenes]

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
