from lab.fast_API.src.application.dtos import (
    OrderDTO,
    OrderItemDTO,
    UpdateOrderStatusDTO,
)
from lab.fast_API.src.application.errors import ForbiddenError, NotFoundError
from lab.fast_API.src.domain.entities import Order
from lab.fast_API.src.domain.ports import UnitOfWorkPort


class UpdateOrderStatusUseCase:
    def __init__(self, uow: UnitOfWorkPort):
        self._uow = uow

    def ejecutar(self, datos: UpdateOrderStatusDTO) -> OrderDTO:
        with self._uow:
            orden = self._uow.orders.get(datos.order_id)
            if orden is None:
                raise NotFoundError(f"Orden {datos.order_id} no encontrada")
            if orden.user_id != datos.requesting_user_id:
                raise ForbiddenError("No tienes permiso para modificar esta orden")

            orden.change_status(datos.status)
            actualizada = self._uow.orders.update_status(orden.id, orden.status)
            self._uow.commit()

            return self._to_dto(actualizada)

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
