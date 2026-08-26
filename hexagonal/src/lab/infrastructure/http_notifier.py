from dominio.entities import Order


class SimulatedHttpNotifier:
    def notificar_orden_creada(self, order: Order) -> bool:
        print(
            f"[HTTP simulado] POST /notificaciones -> "
            f"orden {order.id} creada para usuario {order.user_id} (${order.monto})"
        )
        return True
