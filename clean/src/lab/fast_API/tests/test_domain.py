import pytest
from lab.fast_API.src.domain.entities import Order, OrderItem


def test_order_item_calcula_subtotal():
    item = OrderItem(product_name="Café", quantity=2, unit_price=45.0)
    assert item.subtotal == 90.0


def test_order_item_cantidad_invalida_falla():
    with pytest.raises(ValueError, match="cantidad debe ser mayor a 0"):
        OrderItem(product_name="Café", quantity=0, unit_price=45.0)


def test_order_item_precio_invalido_falla():
    with pytest.raises(ValueError, match="precio unitario debe ser mayor a 0"):
        OrderItem(product_name="Café", quantity=1, unit_price=-5.0)


def test_order_sin_items_falla():
    with pytest.raises(ValueError, match="al menos un artículo"):
        Order.create(user_id=1, items=[])


def test_order_calcula_total_de_varios_items():
    items = [
        OrderItem(product_name="Café", quantity=2, unit_price=45.0),
        OrderItem(product_name="Té", quantity=1, unit_price=30.0),
    ]
    orden = Order.create(user_id=1, items=items)
    assert orden.total == 120.0


def test_order_change_status_valido():
    orden = Order.create(user_id=1, items=[OrderItem("Café", 1, 45.0)])
    orden.change_status("pagado")
    assert orden.status == "pagado"


def test_order_change_status_invalido_falla():
    orden = Order.create(user_id=1, items=[OrderItem("Café", 1, 45.0)])
    with pytest.raises(ValueError, match="Estado inválido"):
        orden.change_status("estado_que_no_existe")


def test_order_pull_events_limpia_la_lista():
    orden = Order.create(user_id=1, items=[OrderItem("Café", 1, 45.0)])
    orden.add_event(object())  # evento genérico, solo para probar el mecanismo

    primeros = orden.pull_events()
    segundos = orden.pull_events()

    assert len(primeros) == 1
    assert segundos == []  # ya se consumieron, no se repiten
