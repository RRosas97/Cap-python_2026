from auth import obtener_usuario_actual
from dependencies import get_db
from fastapi import APIRouter, Depends
from schemas.user import User
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=User)
async def create_new_user(
    user: User,
    db: Session = Depends(get_db),
    usuario_actual: User = Depends(obtener_usuario_actual),
):  # noqa: E501
    return user
