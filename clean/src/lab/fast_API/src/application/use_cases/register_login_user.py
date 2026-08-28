from lab.fast_API.src.application.dtos import (
    LoginDTO,
    RegisterUserDTO,
    TokenDTO,
    UserDTO,
)
from lab.fast_API.src.application.errors import ConflictError, InvalidCredentialsError
from lab.fast_API.src.domain.entities import User
from lab.fast_API.src.domain.ports import (
    PasswordHasherPort,
    TokenProviderPort,
    UnitOfWorkPort,
)


class RegisterUserUseCase:
    def __init__(self, uow: UnitOfWorkPort, hasher: PasswordHasherPort):
        self._uow = uow
        self._hasher = hasher

    def ejecutar(self, datos: RegisterUserDTO) -> UserDTO:
        with self._uow:
            existente = self._uow.users.get_by_username(datos.username)
            if existente is not None:
                raise ConflictError("El username ya está en uso")

            usuario = User(
                username=datos.username,
                email=datos.email,
                hashed_password=self._hasher.hash(datos.password),
            )
            usuario = self._uow.users.add(usuario)
            self._uow.commit()

            return UserDTO(id=usuario.id, 
                           username=usuario.username, 
                           email=usuario.email)


class LoginUseCase:
    def __init__(self, uow: UnitOfWorkPort, 
                 hasher: PasswordHasherPort, 
                 token_provider: TokenProviderPort):
        self._uow = uow
        self._hasher = hasher
        self._token_provider = token_provider

    def ejecutar(self, datos: LoginDTO) -> TokenDTO:
        with self._uow:
            usuario = self._uow.users.get_by_username(datos.username)
            if usuario is None or not self._hasher.verify(
                datos.password, 
                usuario.hashed_password):
                raise InvalidCredentialsError("Usuario o contraseña incorrectos")

            token = self._token_provider.create_token(subject=usuario.username)
            return TokenDTO(access_token=token)
