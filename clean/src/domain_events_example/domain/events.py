from dataclasses import dataclass


@dataclass(frozen=True)
class DomainEvent:
    """
    Clase base para todos los eventos de dominio.
    frozen=True significa que el evento es inmutable:
    una vez creado no puede modificarse.
    """
    pass


@dataclass(frozen=True)
class UsuarioCreado(DomainEvent):
    """
    Se emite cuando un usuario es creado exitosamente.
    Lleva la información mínima que otros necesitan saber.
    """
    user_id: int
    nombre: str
    email: str