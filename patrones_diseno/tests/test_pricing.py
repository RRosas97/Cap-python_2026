import time

from src.scripts.lab.cache_decorator import cache_con_ttl
from src.scripts.lab.providers import (
    AdapterProveedorA,
    AdapterProveedorB,
    ProveedorExternoA,
    ProveedorExternoB,
)
from src.scripts.lab.service import ServicioPrecios
from src.scripts.lab.strategies import PrecioConDescuento, PrecioMayoreo, PrecioRegular

# ---------- Strategy ----------


def test_precio_regular():
    estrategia = PrecioRegular()
    assert estrategia.calcular(precio_base=10.0, cantidad=3) == 30.0


def test_precio_con_descuento():
    estrategia = PrecioConDescuento(porcentaje=0.10)
    assert estrategia.calcular(precio_base=100.0, cantidad=1) == 90.0


def test_precio_mayoreo_por_debajo_del_umbral():
    estrategia = PrecioMayoreo(umbral=10, descuento=0.20)
    assert estrategia.calcular(precio_base=10.0, cantidad=5) == 50.0  # sin descuento


def test_precio_mayoreo_alcanza_umbral():
    estrategia = PrecioMayoreo(umbral=10, descuento=0.20)
    assert estrategia.calcular(precio_base=10.0, cantidad=10) == 80.0  # 100 * 0.8


# ---------- Adapter ----------


def test_adapter_proveedor_a():
    adapter = AdapterProveedorA(ProveedorExternoA())
    assert adapter.obtener_precio_base("CAFE-001") == 45.0


def test_adapter_proveedor_b():
    adapter = AdapterProveedorB(ProveedorExternoB())
    assert adapter.obtener_precio_base("CAFE-001") == 42.5


def test_ambos_adapters_cumplen_el_mismo_contrato():
    """Verificación tipo LSP: ambos deben responder a la misma llamada."""
    adapter_a = AdapterProveedorA(ProveedorExternoA())
    adapter_b = AdapterProveedorB(ProveedorExternoB())

    for adapter in (adapter_a, adapter_b):
        resultado = adapter.obtener_precio_base("TE-002")
        assert isinstance(resultado, float)
        assert resultado > 0


# ---------- Decorator de caché ----------


def test_cache_evita_llamadas_repetidas():
    contador = {"llamadas": 0}

    @cache_con_ttl(segundos=5)
    def funcion_costosa(x):
        contador["llamadas"] += 1
        return x * 2

    funcion_costosa(5)
    funcion_costosa(5)  # debería venir de caché, no incrementar el contador
    funcion_costosa(5)

    assert contador["llamadas"] == 1


def test_cache_distingue_argumentos_distintos():
    contador = {"llamadas": 0}

    @cache_con_ttl(segundos=5)
    def funcion_costosa(x):
        contador["llamadas"] += 1
        return x * 2

    funcion_costosa(5)
    funcion_costosa(10)  # argumento distinto -> debe volver a llamar

    assert contador["llamadas"] == 2


def test_cache_expira_despues_del_ttl():
    contador = {"llamadas": 0}

    @cache_con_ttl(segundos=0.1)  # TTL muy corto, para no alargar la prueba
    def funcion_costosa(x):
        contador["llamadas"] += 1
        return x * 2

    funcion_costosa(5)
    time.sleep(0.2)  # esperamos más que el TTL
    funcion_costosa(5)  # debe volver a llamar, porque ya expiró

    assert contador["llamadas"] == 2


# ---------- Todo junto: el ServicioPrecios ----------


def test_servicio_precios_con_estrategia_regular():
    adapter = AdapterProveedorA(ProveedorExternoA())
    servicio = ServicioPrecios(proveedor=adapter, estrategia=PrecioRegular())

    total = servicio.calcular_precio_final("CAFE-001", cantidad=2)

    assert total == 90.0  # 45.0 * 2


def test_servicio_precios_cambia_de_estrategia_en_caliente():
    adapter = AdapterProveedorA(ProveedorExternoA())
    servicio = ServicioPrecios(proveedor=adapter, estrategia=PrecioRegular())

    total_regular = servicio.calcular_precio_final("CAFE-001", cantidad=2)

    servicio.cambiar_estrategia(PrecioConDescuento(porcentaje=0.5))
    total_con_descuento = servicio.calcular_precio_final("CAFE-001", cantidad=2)

    assert total_con_descuento == total_regular * 0.5


def test_servicio_precios_usa_cache_del_proveedor(monkeypatch):
    llamadas = {"total": 0}

    proveedor_externo = ProveedorExternoA()
    metodo_original = proveedor_externo.get_price

    def get_price_contado(sku):
        llamadas["total"] += 1
        return metodo_original(sku)

    monkeypatch.setattr(proveedor_externo, "get_price", get_price_contado)

    adapter = AdapterProveedorA(proveedor_externo)
    servicio = ServicioPrecios(proveedor=adapter, estrategia=PrecioRegular())

    servicio.calcular_precio_final("CAFE-001", cantidad=1)
    servicio.calcular_precio_final("CAFE-001", cantidad=5)
    # mismo producto, cantidad distinta

    # el PROVEEDOR solo debería llamarse 1 vez -- la segunda vez el precio base
    # viene de caché,
    # aunque la cantidad cambie (la estrategia se aplica después,
    # sobre el precio ya cacheado)
    assert llamadas["total"] == 1
