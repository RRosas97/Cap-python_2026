import pytest
from dominio.entities import Order
from infrastructure.http_notifier import SimulatedHttpNotifier


def crear_notificador_simulado():
    return SimulatedHttpNotifier()


# Estructura parametrizada -- el día que exista un notificador real
# (ej. RealHttpNotifier con httpx), solo se agrega aquí, y esta misma
# batería de pruebas confirma que también cumple el contrato.
IMPLEMENTACIONES = [
    pytest.param(crear_notificador_simulado, id="http_simulado"),
]


@pytest.fixture(params=IMPLEMENTACIONES)
def notificador(request):
    return request.param()


def test_notificar_regresa_true_en_exito(notificador):
    orden = Order.crear(user_id="user-1", monto=100.0)

    resultado = notificador.notificar_orden_creada(orden)

    assert resultado is True


def test_notificar_imprime_informacion_de_la_orden(notificador, capsys):
    orden = Order.crear(user_id="user-1", monto=100.0)

    notificador.notificar_orden_creada(orden)

    salida = capsys.readouterr().out
    assert orden.id in salida
    assert "user-1" in salida
