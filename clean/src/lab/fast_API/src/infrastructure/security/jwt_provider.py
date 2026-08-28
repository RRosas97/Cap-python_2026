from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from lab.fast_API.src.infrastructure.config import settings


class JoseTokenProvider:
    def create_token(self, subject: str) -> str:
        expiracion = datetime.now(timezone.utc) + timedelta(
            minutes=settings.expiracion_minutos)
        payload = {"sub": subject, "exp": expiracion}
        return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

    def decode_token(self, token: str) -> str:
        try:
            payload = jwt.decode(token, settings.secret_key, 
                                 algorithms=[settings.algorithm])
        except JWTError as error:
            raise ValueError(f"Token inválido: {error}")

        subject = payload.get("sub")
        if subject is None:
            raise ValueError("Token sin 'sub'")
        return subject
