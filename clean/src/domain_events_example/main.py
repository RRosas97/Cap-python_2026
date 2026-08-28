from lab.fast_API.src.application.use_cases.create_user import CreateUser
from lab.fast_API.src.domain.events import UsuarioCreado
from fastapi import FastAPI, HTTPException
from lab.fast_API.src.infrastructure.event_bus.in_memory_event_bus import InMemoryEventBus
from lab.fast_API.src.infrastructure.repositories.in_memory_user_repository import InMemoryUserRepository
from pydantic import BaseModel, EmailStr

app = FastAPI()

# ─── Composition root ────────────────────────────────────────────────────────
# Aquí se conectan todas las piezas. Es el único lugar donde
# sabemos qué implementaciones concretas se usan.

repository = InMemoryUserRepository()
event_bus = InMemoryEventBus()


# Handlers: funciones que reaccionan al evento UsuarioCreado.
# El dominio no los conoce; solo sabe que emite un evento.

def enviar_email_bienvenida(evento: UsuarioCreado) -> None:
    print(f"Enviando email de bienvenida a {evento.email}")


def registrar_auditoria(evento: UsuarioCreado) -> None:
    print(f"Auditoría: nuevo usuario {evento.nombre} registrado")


def notificar_crm(evento: UsuarioCreado) -> None:
    print(f"CRM notificado: usuario {evento.nombre} con id {evento.user_id}")


# Se suscriben los handlers al evento.
event_bus.subscribe(UsuarioCreado, enviar_email_bienvenida)
event_bus.subscribe(UsuarioCreado, registrar_auditoria)
event_bus.subscribe(UsuarioCreado, notificar_crm)

create_user = CreateUser(repository, event_bus)

# ─────────────────────────────────────────────────────────────────────────────


class CreateUserRequest(BaseModel):
    nombre: str
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    nombre: str
    email: str


@app.post("/users", response_model=UserResponse, status_code=201)
def crear_usuario(payload: CreateUserRequest):
    try:
        user = create_user.execute(
            user_id=1,
            nombre=payload.nombre,
            email=payload.email,
        )

        return {
            "id": user.id,
            "nombre": user.nombre,
            "email": user.email,
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))