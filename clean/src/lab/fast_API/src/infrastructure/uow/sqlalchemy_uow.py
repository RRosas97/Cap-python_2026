from lab.fast_API.src.infrastructure.db.session import SessionLocal
from lab.fast_API.src.infrastructure.repositories.sqlalchemy_order_repository import (
    SQLAlchemyOrderRepository,
)
from lab.fast_API.src.infrastructure.repositories.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)


class SQLAlchemyUnitOfWork:
    def __init__(self, session_factory=SessionLocal):
        self._session_factory = session_factory

    def __enter__(self):
        self._session = self._session_factory()
        self.orders = SQLAlchemyOrderRepository(self._session)
        self.users = SQLAlchemyUserRepository(self._session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
        self._session.close()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
