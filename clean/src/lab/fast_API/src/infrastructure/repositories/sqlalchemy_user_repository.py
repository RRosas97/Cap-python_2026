from lab.fast_API.src.domain.entities import User
from lab.fast_API.src.infrastructure.db.models import UserModel
from sqlalchemy.orm import Session


class SQLAlchemyUserRepository:
    def __init__(self, session: Session):
        self._session = session

    def add(self, user: User) -> User:
        modelo = UserModel(
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
        )
        self._session.add(modelo)
        self._session.flush()
        return self._a_entidad(modelo)

    def get_by_username(self, username: str) -> User | None:
        modelo = self._session.query(UserModel).filter(
            UserModel.username == username).first()
        return self._a_entidad(modelo) if modelo else None

    def get_by_id(self, user_id: int) -> User | None:
        modelo = self._session.get(UserModel, user_id)
        return self._a_entidad(modelo) if modelo else None

    @staticmethod
    def _a_entidad(modelo: UserModel) -> User:
        return User(
            id=modelo.id,
            username=modelo.username,
            email=modelo.email,
            hashed_password=modelo.hashed_password,
        )
