from typing import Protocol

from dominio.entities import User


class UserRepository(Protocol):
    """
    El PUERTO. Define QUÉ necesita el dominio para persistir usuarios,
    sin decir CÓMO (memoria, SQL, lo que sea). Vive en el dominio porque
    es el dominio quien "pide" este contrato -- la infraestructura
    después viene a cumplirlo, no al revés.
    """

    def guardar(self, usuario: User) -> None: ...

    def obtener(self, user_id: str) -> User | None: ...

    def eliminar(self, user_id: str) -> bool: ...

    def listar(self) -> list[User]: ...
