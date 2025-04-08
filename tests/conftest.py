from datetime import datetime, timezone

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from config import get_database_url
from database import Base, get_async_session
from main import app


@pytest_asyncio.fixture(scope="function")
async def session():
    engine = create_async_engine(get_database_url(True), poolclass=NullPool, future=True)
    async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db_session = async_session_maker()

    yield db_session

    await db_session.close()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest.fixture(autouse=True)
def override_db_dependency(session):
    async def override_get_db():
        yield session

    app.dependency_overrides[get_async_session] = override_get_db

    yield

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def created_table(client):
    payload = {"name": "Table 1", "seats": 1, "location": "У Окна"}
    response = await client.post("/tables", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Table 1"
    assert data["seats"] == 1
    assert data["location"] == "У Окна"

    return data


@pytest_asyncio.fixture
async def created_reservation(client, created_table):
    start_time = datetime.now().isoformat()
    reservation = await client.post("/reservations", json={
        "customer_name": "Dmitry",
        "table_id": created_table["id"],
        "reservation_time": start_time,
        "duration_minutes": 10
    })
    assert reservation.status_code == 201, f"Error: {reservation.status_code}, {reservation.json()}"
    data = reservation.json()
    assert data["customer_name"] == "Dmitry"
    assert data["table_id"] == created_table["id"]
    assert data["reservation_time"] == start_time
    assert data["duration_minutes"] == 10

    return data
