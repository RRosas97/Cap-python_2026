from lab.fast_API.src.application.interfaces.event_bus import EventBus
from lab.fast_API.src.application.interfaces.user_repository import UserRepository
from lab.fast_API.src.domain.user import User


class CreateUser:
    def __init__(
        self,
        repository: UserRepository,
        event_bus: EventBus,
    ):
        self.repository = repository
        self.event_bus = event_bus

    def execute(self, user_id: int, nombre: str, email: str) -> User:
        if self.repository.existe_email(email):
            raise ValueError("El email ya está registrado")

        # La entidad se crea y genera el evento internamente.
        user = User.crear(
            user_id=user_id,
            nombre=nombre,
            email=email,
        )

        # Se persiste el usuario.
        self.repository.guardar(user)

        # Se toman los eventos acumulados en la entidad y se publican.
        # El caso de uso no sabe quién los escucha ni qué hacen.
        for evento in user.pull_events():
            self.event_bus.publish(evento)

        return user