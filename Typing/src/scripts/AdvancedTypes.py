from typing import Literal, Protocol, TypedDict, Union


# Union
def procesar_id(id: Union[int, str]) -> str:
    return f"ID: {id}"


procesar_id(123)  # válido
procesar_id("abc-123")  # también válido


# Sintaxis moderna
def procesar_id(id: int | str) -> str:
    return f"ID: {id}"


# Literal
def cambiar_estado(estado: Literal["pendiente", "pagado", "cancelado"]):
    print(f"Nuevo estado: {estado}")


# TypeDict
class PersonaDict(TypedDict):
    nombre: str
    edad: int


def saludar(persona: PersonaDict):
    print(f"Hola, {persona['nombre']}")


p: PersonaDict = {"nombre": "Ana", "edad": "30"}


# Protocol
class TieneTotal(Protocol):
    total: float


def imprimir_total(objeto: TieneTotal):
    print(f"Total: {objeto.total}")
