from dataclasses import dataclass


@dataclass
class User:
    # Esta entidad solo representa un usuario y sus datos.
    # No sabe nada de FastAPI, bases de datos o HTTP.
    id: int
    name: str
    email: str