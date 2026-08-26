import pytest
from dominio.entities import User


def test_crear_usuario_valido():
    usuario = User.crear(nombre="Ana", email="ana@mail.com")

    assert usuario.nombre == "Ana"
    assert usuario.email == "ana@mail.com"
    assert usuario.id is not None  # se generó un id automáticamente


def test_cada_usuario_tiene_id_unico():
    usuario1 = User.crear(nombre="Ana", email="ana@mail.com")
    usuario2 = User.crear(nombre="Ana", email="ana@mail.com")  # mismos datos

    assert usuario1.id != usuario2.id  # nunca deben coincidir


def test_crear_usuario_con_nombre_vacio_falla():
    with pytest.raises(ValueError, match="nombre no puede estar vacío"):
        User.crear(nombre="", email="ana@mail.com")


def test_crear_usuario_con_nombre_solo_espacios_falla():
    with pytest.raises(ValueError):
        User.crear(nombre="   ", email="ana@mail.com")


def test_crear_usuario_con_email_invalido_falla():
    with pytest.raises(ValueError, match="Email inválido"):
        User.crear(nombre="Ana", email="no-es-un-email")
