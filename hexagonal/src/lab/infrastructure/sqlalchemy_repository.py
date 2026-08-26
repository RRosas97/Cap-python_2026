from dominio.entities import Order
from sqlalchemy import Column, Float, String
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()


class OrderModel(Base):

    __tablename__ = "orders"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    monto = Column(Float, nullable=False)
    estado = Column(String, nullable=False)


class SQLAlchemyOrderRepository:
    def __init__(self, session: Session):
        self._session = session

    def guardar(self, order: Order) -> None:
        modelo = self._session.get(OrderModel, order.id)
        if modelo is None:
            modelo = OrderModel(
                id=order.id,
                user_id=order.user_id,
                monto=order.monto,
                estado=order.estado,
            )
            self._session.add(modelo)
        else:
            modelo.user_id = order.user_id
            modelo.monto = order.monto
            modelo.estado = order.estado
        self._session.commit()

    def obtener(self, order_id: str) -> Order | None:
        modelo = self._session.get(OrderModel, order_id)
        if modelo is None:
            return None
        return self._a_entidad(modelo)

    def listar_por_usuario(self, user_id: str) -> list[Order]:
        modelos = (
            self._session.query(OrderModel).filter(OrderModel.user_id == user_id).all()
        )
        return [self._a_entidad(m) for m in modelos]

    @staticmethod
    def _a_entidad(modelo: OrderModel) -> Order:
        return Order(
            id=modelo.id,
            user_id=modelo.user_id,
            monto=modelo.monto,
            estado=modelo.estado,
        )
