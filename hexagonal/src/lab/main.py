"""
Demo del caso de uso CreateOrder, con dos adapters de repositorio
intercambiables y un notificador HTTP simulado.

Corre con:
    python main.py
"""

from application.dtos import CreateOrderDTO
from application.use_cases import CreateOrderUseCase
from infrastructure.http_notifier import SimulatedHttpNotifier
from infrastructure.memory_repository import InMemoryOrderRepository
from infrastructure.sqlalchemy_repository import Base, SQLAlchemyOrderRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def demo_con_memoria():
    print("=== CreateOrder con repositorio EN MEMORIA ===")
    repositorio = InMemoryOrderRepository()
    notificador = SimulatedHttpNotifier()
    caso_de_uso = CreateOrderUseCase(repositorio, notificador)

    orden = caso_de_uso.ejecutar(CreateOrderDTO(user_id="user-1", monto=150.0))
    print(f"Orden creada: {orden}")

    print(f"Órdenes de user-1: {repositorio.listar_por_usuario('user-1')}")


def demo_con_sqlalchemy():
    print("\n=== CreateOrder con repositorio SQLAlchemy (SQLite en memoria) ===")
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    repositorio = SQLAlchemyOrderRepository(session)
    notificador = SimulatedHttpNotifier()
    caso_de_uso = CreateOrderUseCase(repositorio, notificador)

    orden = caso_de_uso.ejecutar(CreateOrderDTO(user_id="user-2", monto=300.0))
    print(f"Orden creada: {orden}")

    print(f"Órdenes de user-2: {repositorio.listar_por_usuario('user-2')}")


def demo_validacion_falla():
    print("\n=== Probando validación de la entidad (monto inválido) ===")
    repositorio = InMemoryOrderRepository()
    notificador = SimulatedHttpNotifier()
    caso_de_uso = CreateOrderUseCase(repositorio, notificador)

    try:
        caso_de_uso.ejecutar(CreateOrderDTO(user_id="user-1", monto=-50.0))
    except ValueError as error:
        print(f"Error esperado: {error}")


if __name__ == "__main__":
    demo_con_memoria()
    demo_con_sqlalchemy()
    demo_validacion_falla()
