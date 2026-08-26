import pytest
from dominio.entities import Order
from infrastructure.memory_repository import InMemoryOrderRepository
from infrastructure.sqlalchemy_repository import Base, SQLAlchemyOrderRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


def crear_repo_memoria():
    return InMemoryOrderRepository()


def crear_repo_sqlalchemy():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return SQLAlchemyOrderRepository(Session())


IMPLEMENTACIONES = [
    pytest.param(crear_repo_memoria, id="memoria"),
    pytest.param(crear_repo_sqlalchemy, id="sqlalchemy"),
]


@pytest.fixture(params=IMPLEMENTACIONES)
def repositorio(request):
    return request.param()


def test_guardar_y_obtener(repositorio):
    orden = Order.crear(user_id="user-1", monto=100.0)

    repositorio.guardar(orden)
    encontrada = repositorio.obtener(orden.id)

    assert encontrada is not None
    assert encontrada.id == orden.id
    assert encontrada.monto == 100.0


def test_obtener_id_inexistente_regresa_none(repositorio):
    assert repositorio.obtener("id-que-no-existe") is None


def test_listar_por_usuario(repositorio):
    repositorio.guardar(Order.crear(user_id="user-1", monto=100.0))
    repositorio.guardar(Order.crear(user_id="user-1", monto=200.0))
    repositorio.guardar(Order.crear(user_id="user-2", monto=300.0))  # otro usuario

    ordenes_user1 = repositorio.listar_por_usuario("user-1")

    assert len(ordenes_user1) == 2
    assert all(o.user_id == "user-1" for o in ordenes_user1)


def test_listar_usuario_sin_ordenes(repositorio):
    assert repositorio.listar_por_usuario("usuario-fantasma") == []


def test_guardar_sobreescribe_misma_orden(repositorio):
    orden = Order.crear(user_id="user-1", monto=100.0)
    repositorio.guardar(orden)

    orden.estado = "pagada"
    repositorio.guardar(orden)  # mismo id, se actualiza

    encontrada = repositorio.obtener(orden.id)
    assert encontrada.estado == "pagada"
    assert len(repositorio.listar_por_usuario("user-1")) == 1  # no se duplicó
