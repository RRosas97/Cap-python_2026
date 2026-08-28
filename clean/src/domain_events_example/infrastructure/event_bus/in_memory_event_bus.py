from typing import Callable

from lab.fast_API.src.domain.events import DomainEvent


class InMemoryEventBus:
    """
    Bus de eventos simple en memoria.

    Mantiene un registro de handlers por tipo de evento.
    Cuando se publica un evento, llama a todos sus handlers.
    """

    def __init__(self):
        # Diccionario que mapea tipo de evento → lista de funciones.
        self._handlers: dict[type, list[Callable]] = {}

    def subscribe(
        self,
        event_type: type,
        handler: Callable,
    ) -> None:
        """
        Registra una función que reacciona a un tipo de evento.
        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []

        self._handlers[event_type].append(handler)

    def publish(self, event: DomainEvent) -> None:
        """
        Llama a todos los handlers que estén suscritos
        al tipo del evento recibido.
        """
        handlers = self._handlers.get(type(event), [])

        for handler in handlers:
            handler(event)