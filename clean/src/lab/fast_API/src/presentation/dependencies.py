from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from lab.fast_API.src.application.event_handlers import (
    LogOrderCreatedHandler,
    NotifyOrderCreatedHandler,
)
from lab.fast_API.src.application.use_cases.create_order import CreateOrderUseCase
from lab.fast_API.src.application.use_cases.delete_order import DeleteOrderUseCase
from lab.fast_API.src.application.use_cases.get_order import GetOrderUseCase
from lab.fast_API.src.application.use_cases.list_orders import ListOrdersUseCase
from lab.fast_API.src.application.use_cases.register_login_user import (
    LoginUseCase,
    RegisterUserUseCase,
)
from lab.fast_API.src.application.use_cases.update_order_status import (
    UpdateOrderStatusUseCase,
)
from lab.fast_API.src.domain.events import OrderCreated
from lab.fast_API.src.infrastructure.events.in_memory_dispatcher import (
    InMemoryEventDispatcher,
)
from lab.fast_API.src.infrastructure.events.simulated_notifier import (
    SimulatedHttpNotifier,
)
from lab.fast_API.src.infrastructure.security.jwt_provider import JoseTokenProvider
from lab.fast_API.src.infrastructure.security.password_hasher import (
    BcryptPasswordHasher,
)
from lab.fast_API.src.infrastructure.uow.sqlalchemy_uow import SQLAlchemyUnitOfWork

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

_password_hasher = BcryptPasswordHasher()
_token_provider = JoseTokenProvider()

# El dispatcher y sus handlers se registran UNA sola vez, al importar este módulo.
_dispatcher = InMemoryEventDispatcher()
_dispatcher.register(OrderCreated, LogOrderCreatedHandler())
_dispatcher.register(OrderCreated, NotifyOrderCreatedHandler(SimulatedHttpNotifier()))


def get_uow() -> SQLAlchemyUnitOfWork:
    return SQLAlchemyUnitOfWork()


def get_dispatcher() -> InMemoryEventDispatcher:
    return _dispatcher


# ---------- Factories de casos de uso ----------

def get_create_order_use_case(
    uow: SQLAlchemyUnitOfWork = Depends(get_uow),
    dispatcher: InMemoryEventDispatcher = Depends(get_dispatcher),
) -> CreateOrderUseCase:
    return CreateOrderUseCase(uow, dispatcher)


def get_get_order_use_case(
        uow: SQLAlchemyUnitOfWork = Depends(get_uow)) -> GetOrderUseCase:
    return GetOrderUseCase(uow)


def get_list_orders_use_case(
        uow: SQLAlchemyUnitOfWork = Depends(get_uow)) -> ListOrdersUseCase:
    return ListOrdersUseCase(uow)


def get_update_order_status_use_case(
    uow: SQLAlchemyUnitOfWork = Depends(get_uow),
) -> UpdateOrderStatusUseCase:
    return UpdateOrderStatusUseCase(uow)


def get_delete_order_use_case(
        uow: SQLAlchemyUnitOfWork = Depends(get_uow)) -> DeleteOrderUseCase:
    return DeleteOrderUseCase(uow)


def get_register_user_use_case(
    uow: SQLAlchemyUnitOfWork = Depends(get_uow),
) -> RegisterUserUseCase:
    return RegisterUserUseCase(uow, _password_hasher)


def get_login_use_case(uow: SQLAlchemyUnitOfWork = Depends(get_uow)) -> LoginUseCase:
    return LoginUseCase(uow, _password_hasher, _token_provider)


# ---------- Usuario actual autenticado ----------

def get_current_user_id(
    token: str = Depends(oauth2_scheme),
    uow: SQLAlchemyUnitOfWork = Depends(get_uow),
) -> int:
    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username = _token_provider.decode_token(token)
    except ValueError:
        raise credenciales_invalidas

    with uow:
        usuario = uow.users.get_by_username(username)
        if usuario is None:
            raise credenciales_invalidas
        return usuario.id
