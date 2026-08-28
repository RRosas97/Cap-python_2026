from lab.fast_API.src.application.dtos import CreateOrderDTO, OrderDTO, OrderItemDTO
from lab.fast_API.src.domain.entities import Order, OrderItem
from lab.fast_API.src.domain.events import OrderCreated
from lab.fast_API.src.domain.ports import EventDispatcherPort, UnitOfWorkPort


class CreateOrderUseCase:
    def __init__(self, uow: UnitOfWorkPort, dispatcher: EventDispatcherPort):
        self._uow = uow
        self._dispatcher = dispatcher

    def ejecutar(self, datos: CreateOrderDTO) -> OrderDTO:
        items = [
            OrderItem(
                product_name=i.product_name,
                quantity=i.quantity,
                unit_price=i.unit_price,
            )
            for i in datos.items
        ]
        orden = Order.create(user_id=datos.user_id, items=items)

        with self._uow:
            orden = self._uow.orders.add(orden)
            self._uow.commit()
            orden.add_event(
                OrderCreated(
                    order_id=orden.id, user_id=orden.user_id, total=orden.total)
            )
            self._dispatcher.dispatch(orden.pull_events())

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
                    id=item.id,
                    product_name=item.product_name,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    subtotal=item.subtotal,
                )
                for item in orden.items
            ],
            total=orden.total,
        )
