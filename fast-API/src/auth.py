import os
from datetime import datetime, timedelta, timezone

from dependencies import get_db
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from models.user import User
from sqlalchemy.orm import Session

SECRET_KEY = os.environ.get("SECRET_KEY", "123456")
ALGORITHM = "HS256"
EXPIRACION_MINUTOS = 120
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def crear_token(datos: dict) -> str:
    datos_a_codificar = datos.copy()
    expiracion = datetime.now(timezone.utc) + timedelta(minutes=EXPIRACION_MINUTOS)
    datos_a_codificar["exp"] = expiracion
    return jwt.encode(datos_a_codificar, SECRET_KEY, algorithm=ALGORITHM)


def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_db),
) -> User:
    print(f"Token recibido: {token}")
    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Payload decodificado: {payload}")
        username = payload.get("sub")
        if username is None:
            print("No se encontró 'sub' en el payload")
            raise credenciales_invalidas
    except JWTError as error:
        print(f"JWTError: {error}")
        raise credenciales_invalidas

    usuario = session.query(User).filter(User.username == username).first()
    if usuario is None:
        print(f"No se encontró usuario con username: {username}")
        raise credenciales_invalidas

    return usuario
