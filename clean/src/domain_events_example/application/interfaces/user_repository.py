from typing import Protocol

from lab.fast_API.src.domain.user import User


class UserRepository(Protocol):
    def existe_email(self, email: str) -> bool:
        pass

    def guardar(self, user: User) -> None:
        pass