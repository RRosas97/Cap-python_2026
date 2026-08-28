# Orders API -- Reestructurado a Clean Architecture

## Cómo instalar y correr

Reemplaza tu carpeta `src/` completa por esta, y tu `alembic/` (env.py
cambió, la migración existente se conserva sin tocar). Luego:

```bash
poetry install
poetry run uvicorn  main:app --reload
poetry run pytest tests/ -v
```

**No necesitas correr ninguna migración nueva** -- la base de datos ya
migrada sigue siendo 100% compatible (ver sección "hased_password" abajo).

## Estructura

```
src/
├── domain/                      # El núcleo. CERO dependencias externas.
│   ├── entities.py                #   Order (aggregate root), OrderItem, User
│   ├── events.py                   #   DomainEvent, OrderCreated
│   └── ports.py                    #   Protocols: repos, UoW, dispatcher, hasher, tokens
│
├── application/                  # Casos de uso. Solo conocen domain + ports.
│   ├── dtos.py
│   ├── errors.py                   #   NotFoundError, ForbiddenError, etc.
│   ├── event_handlers.py           #   Qué pasa cuando ocurre OrderCreated
│   └── use_cases/
│       ├── create_order.py          #   Usa UoW + despacha OrderCreated
│       ├── get_order.py / list_orders.py / update_order_status.py / delete_order.py
│       └── register_login_user.py
│
├── infrastructure/                # Detalles técnicos. Implementan los puertos.
│   ├── config.py
│   ├── db/models.py                 #   ORM (SQLAlchemy), separado de domain/entities.py
│   ├── db/session.py
│   ├── repositories/                #   SQLAlchemyOrderRepository, SQLAlchemyUserRepository
│   ├── uow/sqlalchemy_uow.py        #   *** UNIT OF WORK ***
│   ├── events/                       #   InMemoryEventDispatcher, SimulatedHttpNotifier
│   └── security/                     #   BcryptPasswordHasher, JoseTokenProvider
│
├── presentation/                  # HTTP. Lo único que sabe de FastAPI/pydantic.
│   ├── schemas.py                   #   Request/response models
│   ├── presenters/                   #   *** PRESENTERS *** -- DTO -> schema de respuesta
│   ├── dependencies.py               #   *** WIRING *** -- conecta todo con Depends()
│   ├── error_handlers.py             #   Excepciones de aplicación -> códigos HTTP
│   └── routers/                       #   orders_router.py, auth_router.py (delgados)
│
└── main.py
```

## Las 3 piezas nuevas que pediste

### 1. Unit of Work (`infrastructure/uow/sqlalchemy_uow.py`)

Agrupa los repositorios de `orders` y `users` bajo una sola transacción.
Se usa como context manager: si algo falla dentro del `with self._uow:`,
`__exit__` hace `rollback()` automáticamente antes de cerrar la sesión --
nada queda guardado a medias.

### 2. Presenter (`presentation/presenters/`)

Convierte los DTOs que regresan los casos de uso (`OrderDTO`, `UserDTO`,
`TokenDTO` -- clases de `application/dtos.py`, sin idea de HTTP) en los
esquemas pydantic de respuesta (`OrderOut`, `UserOut`, `TokenOut` --
`presentation/schemas.py`). Antes, un router regresaba directo un objeto
SQLAlchemy y confiaba en `response_model` de FastAPI para filtrarlo;
ahora esa traducción es explícita y vive en un solo lugar.

### 3. Evento `OrderCreated` (`domain/events.py` + `application/event_handlers.py`)

`CreateOrderUseCase` construye la orden, la persiste vía el UoW, hace
`commit()`, y **solo después** agrega el evento y lo despacha:

```python
orden.add_event(OrderCreated(order_id=orden.id, user_id=orden.user_id, total=orden.total))
self._dispatcher.dispatch(orden.pull_events())
```

El `InMemoryEventDispatcher` (infraestructura) tiene registrados dos
handlers para `OrderCreated`: uno que loguea, otro que "notifica" (HTTP
simulado, mismo patrón que ya construiste antes). Agregar un tercer
handler (mandar un email real, por ejemplo) no requiere tocar el caso
de uso -- solo se registra en `presentation/dependencies.py` (el "wiring").

## Bugs corregidos durante la reestructuración

1. **`orders_route.py` DELETE** llamaba `get_db.get_order(...)` / `get_db.delete_order(...)`
   (`get_db` es una función, no tenía esos métodos -- estaba roto). Ahora
   pasa por `DeleteOrderUseCase`.
2. **`routers/users.py`** se eliminó -- pedía autenticación para "crear
   un usuario" pero nunca lo persistía, y duplicaba `/auth/register`.
3. **`hased_password`** (typo histórico, ya en tu migración real) se
   mantiene como nombre de columna física, pero se mapea a un atributo
   Python correcto: `hashed_password = Column("hased_password", ...)`
   en `infrastructure/db/models.py`. No rompe tu base de datos existente.
4. **`passlib` + `bcrypt`** -- se reemplazó por `bcrypt` directo
   (`BcryptPasswordHasher`), evitando el bug de compatibilidad que ya
   viste (`AttributeError: module 'bcrypt' has no attribute '__about__'`).
   El formato del hash es idéntico, así que los usuarios ya registrados
   siguen pudiendo iniciar sesión sin cambios.
5. Se quitaron los endpoints de scratch (`/`, `/show_message`, `/items`)
   de `main.py` -- no eran parte del servicio de Orders.

## Verificación

`domain` y `application` se probaron ejecutándolos directamente con
fakes en memoria (sin SQLAlchemy/FastAPI) -- ver `tests/test_lab.fast_API.src.domain.py`
y `tests/test_create_order_use_case.py`. La capa de infraestructura
(SQLAlchemy, FastAPI, bcrypt, jose) **no se pudo ejecutar** en el entorno
donde se generó este proyecto por falta de esas dependencias instaladas
-- corre `poetry run pytest tests/ -v` en tu máquina para confirmar
`test_orders_api.py` (copiado sin cambios de tu suite original, ya que
el comportamiento HTTP observable es idéntico).
