from lab.fast_API.src.domain.user import User


class InMemoryUserRepository:
    def __init__(self):
        self._users: list[User] = []

    def existe_email(self, email: str) -> bool:
        return any(user.email == email for user in self._users)

    def guardar(self, user: User) -> None:
        self._users.append(user)