import uuid
from dataclasses import dataclass


@dataclass
class User:
    """
    La ENTIDAD. Vive en el centro del hexágono.
    No sabe nada de bases de datos, HTTP, ni de cómo se guarda o se expone.
    Solo conoce las reglas de negocio que le pertenecen a ella misma.
    """

    id: str
    nombre: str
    email: str

    @staticmethod
    def crear(nombre: str, email: str) -> "User":
        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        if "@" not in email:
            raise ValueError("Email inválido")
        return User(id=str(uuid.uuid4()), nombre=nombre, email=email)
