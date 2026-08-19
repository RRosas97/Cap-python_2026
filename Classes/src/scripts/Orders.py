from dataclasses import dataclass

from pydantic import BaseModel


@dataclass(order=True)
class Order:
    cantidad: int
    precio_unitario: float
    id: int = 0

    @property
    def total(self):
        return self.cantidad * self.precio_unitario


class OrderIn(BaseModel):
    cantidad: int
    precio_unitario: float


class OrderOut(BaseModel):
    id: int
    cantidad: int
    precio_unitario: float
    total: float


def crear_order(datos_json: dict, siguiente_id: int) -> Order:
    order_in = OrderIn(**datos_json)
    return Order(
        cantidad=order_in.cantidad,
        precio_unitario=order_in.precio_unitario,
        id=siguiente_id,
    )


def order_a_salida(order: Order) -> OrderOut:
    return OrderOut(
        id=order.id,
        cantidad=order.cantidad,
        precio_unitario=order.precio_unitario,
        total=order.total,
    )


data = {"cantidad": 3, "precio_unitario": 10.5}

order = crear_order(data, siguiente_id=1)

print(order)
print(order.total)

salida = order_a_salida(order)
print(salida)
print(salida.model_dump())

otro_order = Order(cantidad=5, precio_unitario=2.0, id=2)
print(order < otro_order)
print(order == otro_order)
