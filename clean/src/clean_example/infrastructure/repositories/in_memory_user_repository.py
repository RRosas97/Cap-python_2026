from lab.fast_API.src.domain.user import User


class InMemoryUserRepository:
    """
    Implementación concreta del contrato UserRepository.

    En un proyecto real podrías tener otra implementación llamada
    SQLServerUserRepository que use pyodbc o SQLAlchemy.
    """

    def __init__(self):
        # Simula una tabla de usuarios con una lista.
        self._users: list[User] = []

    def get_by_email(self, email: str) -> User | None:
        # Busca el primer usuario con ese email.
        for user in self._users:
            if user.email == email:
                return user

        # Si no existe, devuelve None.
        return None

    def save(self, user: User) -> None:
        # En lugar de INSERT INTO users..., guardamos en memoria.
        self._users.append(user)