from typing import Protocol

from lab.fast_API.src.domain.user import User


class UserRepository(Protocol):
    """
    Contrato que necesita la aplicación.

    No importa si los usuarios se guardan en SQL Server, PostgreSQL,
    un archivo o memoria. Cualquier implementación que cumpla estos
    métodos puede utilizarse.
    """

    def get_by_email(self, email: str) -> User | None:
        ...

    def save(self, user: User) -> None:
        ...