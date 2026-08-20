# src/routers/auth.py
from auth import crear_token
from dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models.user import User
from passlib.context import CryptContext
from schemas.auth import Token
from schemas.user import UserCreate, UserOut
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", response_model=UserOut)
def registrar_usuario(datos: UserCreate, session: Session = Depends(get_db)):
    existente = session.query(User).filter(User.username == datos.username).first()
    if existente:
        raise HTTPException(status_code=400, detail="El username ya está en uso")

    nuevo_usuario = User(
        username=datos.username,
        email=datos.email,
        hased_password=pwd_context.hash(datos.password),
    )
    session.add(nuevo_usuario)
    session.commit()
    session.refresh(nuevo_usuario)

    return nuevo_usuario


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_db),
):
    usuario = session.query(User).filter(User.username == form_data.username).first()

    if usuario is None or not pwd_context.verify(
        form_data.password, usuario.hased_password
    ):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    token = crear_token({"sub": usuario.username})
    return Token(access_token=token)
