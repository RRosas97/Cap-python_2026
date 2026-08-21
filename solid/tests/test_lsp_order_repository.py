import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from src.scripts.Lab.memory_order_repository import InMemoryOrderRepository
from src.scripts.Lab.models.base import Base
from src.scripts.Lab.models.user import User
from src.scripts.Lab.order_service import OrderService
from src.scripts.Lab.sql_order_repository import SQLOrderRepository


def crear_repo_memoria():
    return InMemoryOrderRepository()


def crear_repo_sql():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    usuario = User(username="test", email="test@mail.com", hased_password="x")
    session.add(usuario)
    session.commit()

    return SQLOrderRepository(session)


IMPLEMENTACIONES = [
    pytest.param(crear_repo_memoria, id="memoria"),
    pytest.param(crear_repo_sql, id="sql"),
]


@pytest.fixture(params=IMPLEMENTACIONES)
def servicio(request):
    repo_factory = request.param
    repo = repo_factory()
    return OrderService(repo)


def test_crear_orden(servicio):
    orden = servicio.crear_orden(user_id=1)

    assert orden.id is not None
    assert orden.status == "pendiente"
    assert orden.user_id == 1


def test_obtener_orden_existente(servicio):
    creada = servicio.crear_orden(user_id=1)

    encontrada = servicio.obtener_orden(creada.id)

    assert encontrada is not None
    assert encontrada.id == creada.id


def test_obtener_orden_inexistente(servicio):
    resultado = servicio.obtener_orden(9999)
    assert resultado is None


def test_listar_ordenes_de_usuario(servicio):
    servicio.crear_orden(user_id=1)
    servicio.crear_orden(user_id=1)
    servicio.crear_orden(user_id=1)

    ordenes = servicio.listar_ordenes_de_usuario(user_id=1)

    assert len(ordenes) == 3


def test_marcar_como_pagada(servicio):
    orden = servicio.crear_orden(user_id=1)

    actualizada = servicio.marcar_como_pagada(orden.id)

    assert actualizada.status == "pagado"


def test_cancelar_orden(servicio):
    orden = servicio.crear_orden(user_id=1)

    eliminada = servicio.cancelar_orden(orden.id)

    assert eliminada is True
    assert servicio.obtener_orden(orden.id) is None


def test_cancelar_orden_inexistente(servicio):
    resultado = servicio.cancelar_orden(9999)
    assert resultado is False
