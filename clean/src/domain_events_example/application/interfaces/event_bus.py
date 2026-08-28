from typing import Protocol

from lab.fast_API.src.domain.events import DomainEvent


class EventBus(Protocol):
    """
    Contrato para publicar eventos de dominio.

    El caso de uso solo conoce este contrato, no sabe si
    los eventos van a una cola, a Redis, a Kafka o a memoria.
    """

    def publish(self, event: DomainEvent) -> None:
        pass