import logging

from lab.fast_API.src.domain.events import OrderCreated

logger = logging.getLogger("orders")


class LogOrderCreatedHandler:
    def __call__(self, event: OrderCreated) -> None:
        logger.info(
            "Orden creada: id=%s, user_id=%s, total=%.2f",
            event.order_id, event.user_id, event.total,
        )


class NotifyOrderCreatedHandler:
    """No sabe si la notificación real es HTTP, email, SMS -- solo pide
    que 'algo' notifique, a través del puerto que le inyectemos."""

    def __init__(self, notifier):
        self._notifier = notifier

    def __call__(self, event: OrderCreated) -> None:
        self._notifier.notificar_orden_creada(event)
