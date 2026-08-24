from typing import Protocol


class ProveedorPrecios(Protocol):

    def obtener_precio_base(self, producto: str) -> float: ...


class ProveedorExternoA:

    def get_price(self, sku: str) -> float:
        precios = {"CAFE-001": 45.0, "TE-002": 30.0}
        return precios.get(sku, 0.0)


class ProveedorExternoB:

    def fetch_cost(self, item_code: str) -> dict:
        precios = {
            "CAFE-001": {"cost": 42.5, "currency": "MXN"},
            "TE-002": {"cost": 28.0, "currency": "MXN"},
        }
        return precios.get(item_code, {"cost": 0.0, "currency": "MXN"})


class AdapterProveedorA:
    def __init__(self, proveedor: ProveedorExternoA):
        self._proveedor = proveedor

    def obtener_precio_base(self, producto: str) -> float:
        return self._proveedor.get_price(sku=producto)


class AdapterProveedorB:
    def __init__(self, proveedor: ProveedorExternoB):
        self._proveedor = proveedor

    def obtener_precio_base(self, producto: str) -> float:
        resultado = self._proveedor.fetch_cost(item_code=producto)
        return resultado["cost"]
