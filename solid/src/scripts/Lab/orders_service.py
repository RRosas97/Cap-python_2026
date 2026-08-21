from sqlalchemy.orm import Session
from src.scripts.Lab.models.order import Order
from src.scripts.Lab.models.order_item import OrderItem


def create_order(session: Session, user_id: int, status: str = "pendiente") -> Order:
    order = Order(user_id=user_id, status=status)
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


def create_order_with_items(session: Session, user_id: int, items: list[dict]) -> Order:
    """items: lista de dicts con product_name, quantity, unit_price."""
    order = Order(user_id=user_id, status="pendiente")
    session.add(order)
    session.flush()

    for item_data in items:
        item = OrderItem(order_id=order.id, **item_data)
        session.add(item)

    session.commit()
    session.refresh(order)
    return order


def list_orders_by_user(session: Session, user_id: int) -> list[Order]:
    return session.query(Order).filter(Order.user_id == user_id).all()


def get_order(session: Session, order_id: int) -> Order | None:
    return session.get(Order, order_id)


def update_order_status(session: Session, order_id: int, status: str) -> Order | None:
    order = session.get(Order, order_id)
    if order is None:
        return None
    order.status = status
    session.commit()
    session.refresh(order)
    return order


def delete_order(session: Session, order_id: int) -> bool:
    order = session.get(Order, order_id)
    if order is None:
        return False
    session.delete(order)
    session.commit()
    return True
