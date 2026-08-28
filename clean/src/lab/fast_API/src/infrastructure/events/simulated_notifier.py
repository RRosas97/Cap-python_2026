from lab.fast_API.src.domain.events import OrderCreated


class SimulatedHttpNotifier:
    def notificar_orden_creada(self, event: OrderCreated) -> bool:
        print(
            f"[HTTP simulado] POST /notificaciones -> "
            f"orden {event.order_id} creada para usuario {event.user_id} (${event.total})"  # noqa: E501
        )
        return True
