from dataclasses import dataclass, field
from datetime import datetime, timezone


class DomainEvent:
    pass


@dataclass
class OrderCreated(DomainEvent):
    order_id: int
    user_id: int
    total: float
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
