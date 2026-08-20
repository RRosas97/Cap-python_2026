import pytest
from dependencies import get_db
from httpx import ASGITransport, AsyncClient
from main import app
from models.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


@pytest.fixture
def test_engine():
    """
    SQLite en memoria, compartida entre conexiones con StaticPool.

    Sin StaticPool, cada nueva conexión a ':memory:' crearía una BD
    NUEVA y vacía -- tu app y tus asserts verían bases de datos distintas.
    StaticPool fuerza a que todos reutilicen la MISMA conexión/BD en memoria.
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture
async def client(test_engine):
    TestingSessionLocal = sessionmaker(bind=test_engine)

    def override_get_db():
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as cliente:
        yield cliente

    app.dependency_overrides.clear()
