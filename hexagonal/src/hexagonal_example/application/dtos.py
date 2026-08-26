from dataclasses import dataclass


@dataclass
class CrearUsuarioDTO:
    """Lo que ENTRA a un caso de uso -- datos crudos, sin identidad todavía."""

    nombre: str
    email: str


@dataclass
class UsuarioDTO:
    """Lo que SALE de un caso de uso -- una foto de los datos del usuario,
    sin exponer la entidad completa ni su comportamiento."""

    id: str
    nombre: str
    email: str
