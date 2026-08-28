from lab.fast_API.src.application.interfaces.user_repository import UserRepository
from lab.fast_API.src.domain.user import User


class CreateUser:
    """
    Caso de uso: coordina la acción de crear un usuario.

    Aquí vive la regla de negocio:
    no se permite repetir un email.
    """

    def __init__(self, repository: UserRepository):
        # Recibimos una abstracción, no una base de datos concreta.
        self.repository = repository

    def execute(self, user_id: int, name: str, email: str) -> User:
        # Pregunta al repositorio si ya existe un usuario con ese email.
        existing_user = self.repository.get_by_email(email)

        if existing_user is not None:
            raise ValueError("El email ya está registrado")

        # Crea la entidad del dominio.
        new_user = User(
            id=user_id,
            name=name,
            email=email,
        )

        # Pide guardar el usuario sin conocer cómo se persiste.
        self.repository.save(new_user)

        return new_user