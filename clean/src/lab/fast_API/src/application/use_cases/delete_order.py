from lab.fast_API.src.application.errors import ForbiddenError, NotFoundError
from lab.fast_API.src.domain.ports import UnitOfWorkPort


class DeleteOrderUseCase:
    def __init__(self, uow: UnitOfWorkPort):
        self._uow = uow

    def ejecutar(self, order_id: int, requesting_user_id: int) -> None:
        with self._uow:
            orden = self._uow.orders.get(order_id)
            if orden is None:
                raise NotFoundError(f"Orden {order_id} no encontrada")
            if orden.user_id != requesting_user_id:
                raise ForbiddenError("No tienes permiso para eliminar esta orden")

            self._uow.orders.delete(order_id)
            self._uow.commit()
