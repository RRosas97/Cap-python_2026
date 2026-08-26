from dominio.entities import User


class InMemoryUserRepository:
    """
    El ADAPTER. Vive en infraestructura porque es un detalle técnico
    (aquí, un diccionario en RAM) -- mañana podría ser SQLOrderRepository
    o MongoUserRepository, y el dominio/application NUNCA se enterarían
    del cambio, porque ambos solo conocen el puerto (UserRepository).
    """

    def __init__(self):
        self._usuarios: dict[str, User] = {}

    def guardar(self, usuario: User) -> None:
        self._usuarios[usuario.id] = usuario

    def obtener(self, user_id: str) -> User | None:
        return self._usuarios.get(user_id)

    def eliminar(self, user_id: str) -> bool:
        if user_id not in self._usuarios:
            return False
        del self._usuarios[user_id]
        return True

    def listar(self) -> list[User]:
        return list(self._usuarios.values())
