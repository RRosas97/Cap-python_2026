import pytest
from application.dtos import CreateOrderDTO
from application.use_cases import CreateOrderUseCase
from infrastructure.memory_repository import InMemoryOrderRepository


class NotificadorEspia:
    """
    Un 'test double': no notifica de verdad, solo RECUERDA que lo llamaron
    y con qué datos -- para poder verificar la orquestación del caso de uso
    sin depender de la implementación real del notificador.
    """

    def __init__(self):
        self.llamadas = []

    def notificar_orden_creada(self, order) -> bool:
        self.llamadas.append(order)
        return True


@pytest.fixture
def caso_de_uso():
    repositorio = InMemoryOrderRepository()
    notificador = NotificadorEspia()
    caso_de_uso = CreateOrderUseCase(repositorio, notificador)
    return caso_de_uso, repositorio, notificador


def test_create_order_guarda_la_orden(caso_de_uso):
    uc, repositorio, _ = caso_de_uso

    resultado = uc.ejecutar(CreateOrderDTO(user_id="user-1", monto=150.0))

    guardada = repositorio.obtener(resultado.id)
    assert guardada is not None
    assert guardada.monto == 150.0


def test_create_order_notifica_exactamente_una_vez(caso_de_uso):
    uc, _, notificador = caso_de_uso

    uc.ejecutar(CreateOrderDTO(user_id="user-1", monto=150.0))

    assert len(notificador.llamadas) == 1
    assert notificador.llamadas[0].user_id == "user-1"


def test_create_order_regresa_dto_correcto(caso_de_uso):
    uc, _, _ = caso_de_uso

    resultado = uc.ejecutar(CreateOrderDTO(user_id="user-1", monto=150.0))

    assert resultado.user_id == "user-1"
    assert resultado.monto == 150.0
    assert resultado.estado == "creada"


def test_create_order_con_monto_invalido_no_notifica(caso_de_uso):
    """Si la entidad rechaza los datos, el flujo debe detenerse ANTES de notificar."""
    uc, repositorio, notificador = caso_de_uso

    with pytest.raises(ValueError):
        uc.ejecutar(CreateOrderDTO(user_id="user-1", monto=-50.0))

    assert notificador.llamadas == []
    assert repositorio.listar_por_usuario("user-1") == []
