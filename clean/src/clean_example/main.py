from lab.fast_API.src.application.use_cases.create_user import CreateUser
from fastapi import FastAPI, HTTPException
from lab.fast_API.src.infrastructure.repositories.in_memory_user_repository import InMemoryUserRepository
from pydantic import BaseModel, EmailStr

app = FastAPI()

# En esta capa se conectan las piezas de la aplicación.
# A esto también se le puede llamar "wiring" o composition root.
repository = InMemoryUserRepository()
create_user = CreateUser(repository)


class CreateUserRequest(BaseModel):
    # Pydantic valida que el valor recibido sea un email válido.
    name: str
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    name: str
    email: str


@app.post("/users", response_model=UserResponse, status_code=201)
def create_user_endpoint(payload: CreateUserRequest):
    try:
        # La ruta transforma la petición HTTP en una llamada al caso de uso.
        user = create_user.execute(
            user_id=1,  # En una aplicación real se generaría de otra forma.
            name=payload.name,
            email=payload.email,
        )

        # FastAPI transforma este diccionario en JSON de respuesta.
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        }

    except ValueError as error:
        # La capa HTTP decide cómo expresar el error hacia el cliente.
        raise HTTPException(status_code=400, detail=str(error))