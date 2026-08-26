from dominio.entities import User
from dominio.ports import UserRepository

from application.dtos import CrearUsuarioDTO, UsuarioDTO


class CrearUsuarioUseCase:
    """
    Un CASO DE USO = una acción completa del sistema.
    Orquesta: recibe un DTO, construye la Entidad, la guarda vía el puerto,
    y regresa otro DTO. Nunca sabe si el repositorio es memoria o SQL.
    """

    def __init__(self, repositorio: UserRepository):
        self._repositorio = repositorio

    def ejecutar(self, datos: CrearUsuarioDTO) -> UsuarioDTO:
        usuario = User.crear(nombre=datos.nombre, email=datos.email)
        self._repositorio.guardar(usuario)
        return UsuarioDTO(id=usuario.id, nombre=usuario.nombre, email=usuario.email)


class EliminarUsuarioUseCase:
    def __init__(self, repositorio: UserRepository):
        self._repositorio = repositorio

    def ejecutar(self, user_id: str) -> bool:
        return self._repositorio.eliminar(user_id)


class ListarUsuariosUseCase:
    def __init__(self, repositorio: UserRepository):
        self._repositorio = repositorio

    def ejecutar(self) -> list[UsuarioDTO]:
        return [
            UsuarioDTO(id=u.id, nombre=u.nombre, email=u.email)
            for u in self._repositorio.listar()
        ]
