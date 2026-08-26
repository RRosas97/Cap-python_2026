from dominio.entities import Order
from dominio.ports import NotificationPort, OrderRepository

from application.dtos import CreateOrderDTO, OrderDTO


class CreateOrderUseCase:
    def __init__(self, repositorio: OrderRepository, notificador: NotificationPort):
        self._repositorio = repositorio
        self._notificador = notificador

    def ejecutar(self, datos: CreateOrderDTO) -> OrderDTO:
        orden = Order.crear(user_id=datos.user_id, monto=datos.monto)
        self._repositorio.guardar(orden)
        self._notificador.notificar_orden_creada(orden)

        return OrderDTO(
            id=orden.id, user_id=orden.user_id, monto=orden.monto, estado=orden.estado
        )
