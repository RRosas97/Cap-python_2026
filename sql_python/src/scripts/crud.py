from sqlalchemy.orm import Session

from src.models import Order, OrderItem, User

# ---------- User ----------


def create_user(session: Session, username: str, email: str) -> User:
    user = User(username=username, email=email)
    session.add(user)
    session.commit()
    session.refresh(user)  # trae el id generado por la BD
    return user


def get_user(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)


def list_users(session: Session) -> list[User]:
    return session.query(User).all()


def update_user(session: Session, user_id: int, **campos) -> User | None:
    user = session.get(User, user_id)
    if user is None:
        return None
    for clave, valor in campos.items():
        setattr(user, clave, valor)
    session.commit()
    session.refresh(user)
    return user


def delete_user(session: Session, user_id: int) -> bool:
    user = session.get(User, user_id)
    if user is None:
        return False
    session.delete(user)
    session.commit()
    return True


# ---------- Order ----------


def create_order(session: Session, user_id: int, status: str = "pendiente") -> Order:
    order = Order(user_id=user_id, status=status)
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


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


# ---------- OrderItem ----------


def add_item_to_order(
    session: Session, order_id: int, product_name: str, quantity: int, unit_price: float
) -> OrderItem:
    item = OrderItem(
        order_id=order_id,
        product_name=product_name,
        quantity=quantity,
        unit_price=unit_price,
    )
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def remove_item(session: Session, item_id: int) -> bool:
    item = session.get(OrderItem, item_id)
    if item is None:
        return False
    session.delete(item)
    session.commit()
    return True
