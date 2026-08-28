from dataclasses import dataclass, field

from lab.fast_API.src.domain.events import DomainEvent, UsuarioCreado


@dataclass
class User:
    id: int
    nombre: str
    email: str

    # La entidad acumula los eventos que generó.
    # No los publica directamente: solo los guarda.
    _events: list[DomainEvent] = field(
        default_factory=list,
        repr=False,
    )

    @staticmethod
    def crear(user_id: int, nombre: str, email: str) -> "User":
        """
        Método de fábrica: crea el usuario y emite el evento.
        En Clean Architecture las reglas de creación viven aquí.
        """
        user = User(id=user_id, nombre=nombre, email=email)

        # La entidad registra que algo importante ocurrió.
        user._events.append(
            UsuarioCreado(
                user_id=user_id,
                nombre=nombre,
                email=email,
            )
        )

        return user

    def pull_events(self) -> list[DomainEvent]:
        """
        Devuelve los eventos pendientes y los limpia.
        El caso de uso los toma de aquí para publicarlos.
        """
        eventos = list(self._events)
        self._events.clear()
        return eventos