import src.scripts.Lab.orders_service as crud
from sqlalchemy.orm import Session
from src.scripts.Lab.models.order import Order


class SQLOrderRepository:

    def __init__(self, session: Session):
        self._session = session

    def add(self, order: Order) -> Order:
        self._session.add(order)
        self._session.commit()
        self._session.refresh(order)
        return order

    def get(self, order_id: int) -> Order | None:
        return crud.get_order(self._session, order_id)

    def list_by_user(self, user_id: int) -> list[Order]:
        return crud.list_orders_by_user(self._session, user_id)

    def update_status(self, order_id: int, status: str) -> Order | None:
        return crud.update_order_status(self._session, order_id, status)

    def delete(self, order_id: int) -> bool:
        return crud.delete_order(self._session, order_id)
