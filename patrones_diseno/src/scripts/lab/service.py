from src.scripts.lab.cache_decorator import cache_con_ttl
from src.scripts.lab.providers import ProveedorPrecios
from src.scripts.lab.strategies import EstrategiaPrecio


class ServicioPrecios:
    def __init__(self, proveedor: ProveedorPrecios, estrategia: EstrategiaPrecio):
        self._proveedor = proveedor
        self._estrategia = estrategia

    @cache_con_ttl(segundos=5)
    def _obtener_precio_base(self, producto: str) -> float:
        return self._proveedor.obtener_precio_base(producto)

    def calcular_precio_final(self, producto: str, cantidad: int) -> float:
        precio_base = self._obtener_precio_base(producto)
        return self._estrategia.calcular(precio_base, cantidad)

    def cambiar_estrategia(self, nueva: EstrategiaPrecio) -> None:
        self._estrategia = nueva
