from collections import defaultdict

from lab.fast_API.src.domain.events import DomainEvent


class InMemoryEventDispatcher:
    def __init__(self):
        self._handlers: dict[type, list] = defaultdict(list)

    def register(self, event_type: type, handler) -> None:
        self._handlers[event_type].append(handler)

    def dispatch(self, events: list[DomainEvent]) -> None:
        for event in events:
            for handler in self._handlers[type(event)]:
                handler(event)
