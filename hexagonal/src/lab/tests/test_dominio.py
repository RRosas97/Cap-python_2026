import pytest
from dominio.entities import Order


def test_crear_orden_valida():
    orden = Order.crear(user_id="user-1", monto=100.0)

    assert orden.user_id == "user-1"
    assert orden.monto == 100.0
    assert orden.estado == "creada"
    assert orden.id is not None


def test_cada_orden_tiene_id_unico():
    orden1 = Order.crear(user_id="user-1", monto=100.0)
    orden2 = Order.crear(user_id="user-1", monto=100.0)

    assert orden1.id != orden2.id


def test_crear_orden_con_monto_cero_falla():
    with pytest.raises(ValueError, match="monto debe ser mayor a 0"):
        Order.crear(user_id="user-1", monto=0)


def test_crear_orden_con_monto_negativo_falla():
    with pytest.raises(ValueError, match="monto debe ser mayor a 0"):
        Order.crear(user_id="user-1", monto=-50.0)


def test_crear_orden_con_user_id_vacio_falla():
    with pytest.raises(ValueError, match="user_id no puede estar vacío"):
        Order.crear(user_id="", monto=100.0)
