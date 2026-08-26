import pytest
from dominio.entities import User
from infrastructure.memory_repository import InMemoryUserRepository


def crear_repo_memoria():
    return InMemoryUserRepository()


# Lista de fábricas de adapters a probar. El día que exista un
# SQLUserRepository real, solo se agrega aquí, y automáticamente
# corre TODA esta batería de pruebas contra él también.
IMPLEMENTACIONES = [
    pytest.param(crear_repo_memoria, id="memoria"),
]


@pytest.fixture(params=IMPLEMENTACIONES)
def repositorio(request):
    return request.param()


def test_guardar_y_obtener(repositorio):
    usuario = User.crear(nombre="Ana", email="ana@mail.com")

    repositorio.guardar(usuario)
    encontrado = repositorio.obtener(usuario.id)

    assert encontrado is not None
    assert encontrado.id == usuario.id
    assert encontrado.nombre == "Ana"


def test_obtener_id_inexistente_regresa_none(repositorio):
    resultado = repositorio.obtener("id-que-no-existe")
    assert resultado is None


def test_listar_regresa_todos_los_guardados(repositorio):
    repositorio.guardar(User.crear(nombre="Ana", email="ana@mail.com"))
    repositorio.guardar(User.crear(nombre="Luis", email="luis@mail.com"))

    usuarios = repositorio.listar()

    assert len(usuarios) == 2
    nombres = {u.nombre for u in usuarios}
    assert nombres == {"Ana", "Luis"}


def test_listar_repositorio_vacio(repositorio):
    assert repositorio.listar() == []


def test_eliminar_usuario_existente(repositorio):
    usuario = User.crear(nombre="Ana", email="ana@mail.com")
    repositorio.guardar(usuario)

    eliminado = repositorio.eliminar(usuario.id)

    assert eliminado is True
    assert repositorio.obtener(usuario.id) is None


def test_eliminar_usuario_inexistente_regresa_false(repositorio):
    resultado = repositorio.eliminar("id-que-no-existe")
    assert resultado is False


def test_guardar_sobreescribe_si_mismo_id(repositorio):
    usuario = User.crear(nombre="Ana", email="ana@mail.com")
    repositorio.guardar(usuario)

    usuario.nombre = "Ana Actualizada"  # se modifica el mismo objeto
    repositorio.guardar(usuario)  # se vuelve a guardar, mismo id

    encontrado = repositorio.obtener(usuario.id)
    assert encontrado.nombre == "Ana Actualizada"
    assert len(repositorio.listar()) == 1  # no se duplicó
