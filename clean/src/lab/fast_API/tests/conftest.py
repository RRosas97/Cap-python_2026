import pytest
from httpx import ASGITransport, AsyncClient
from lab.fast_API.src.infrastructure.db.models import Base
from lab.fast_API.src.infrastructure.repositories.sqlalchemy_order_repository import (
    SQLAlchemyOrderRepository,
)
from lab.fast_API.src.infrastructure.repositories.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from lab.fast_API.src.main import app
from lab.fast_API.src.presentation.dependencies import get_uow
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


@pytest.fixture
def test_engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


class _TestUnitOfWork:
    def __init__(self, session_factory):
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

    def commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()


@pytest.fixture
async def client(test_engine):
    TestingSessionLocal = sessionmaker(bind=test_engine)

    def override_get_uow():
        return _TestUnitOfWork(TestingSessionLocal)

    app.dependency_overrides[get_uow] = override_get_uow

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as cliente:
        yield cliente

    app.dependency_overrides.clear()
