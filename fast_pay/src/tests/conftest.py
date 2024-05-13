"""
run tests with command to skip docker-volume:

pytest . --ignore=volumes/db/

"""

import os
from datetime import datetime
from decimal import Decimal

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from src.database import get_session
from src.main import app
from src.models import Account, Provider, Service, Wallet

load_dotenv()

pytest.test_provider_email = "company_test@mail.com"
pytest.test_provider_client_id = "D3H6P3WM"
pytest.test_provider_client_secret = "lOE54vkjqjPH8F8SqSQuDHPW"
pytest.test_provider_service_id = "SERV_t7Iad3DkPrq"
pytest.test_provider_service_price = Decimal("10.0")

pytest.test_wallet_email = "customer_test@mail.com"
pytest.test_wallet_customer_uuid = "jdtidF6dWfZu7emkSPm7xY"
pytest.test_wallet_balance = Decimal("100.0")

pytest.test_account_number = "NFQWfg9jP1Q408oS5azJQm"

TEST_DB_NAME = f"{os.getenv('DB_NAME')}_test"
TEST_DB_URL = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{TEST_DB_NAME}"
FAKE_DB_URL = f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{TEST_DB_NAME}"
REAL_DB_URL = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"


def db_prep():
    engine = create_engine(REAL_DB_URL)
    conn = engine.connect()
    try:
        conn = conn.execution_options(autocommit=False)
        conn.execute(text("ROLLBACK"))
        conn.execute(text(f"DROP DATABASE {TEST_DB_NAME};"))
    except ProgrammingError:
        conn.execute(text("ROLLBACK"))
    except OperationalError:
        conn.execute(text("ROLLBACK"))
    conn.execute(text(f"CREATE DATABASE {TEST_DB_NAME};"))
    conn.close()


async def fake_db_session():
    engine = create_async_engine(FAKE_DB_URL, future=True, echo=False)
    async_session = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        yield session


@pytest.fixture(scope="function")
def fake_session_maker():
    engine = create_async_engine(FAKE_DB_URL, future=True, echo=False)
    async_session = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    return async_session


@pytest.fixture(scope="session", autouse=True)
def fake_db():
    db_prep()
    engine = create_engine(TEST_DB_URL)
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    from src.models import Base

    db = session_local()
    Base.metadata.create_all(engine)
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def fake_provider(fake_db):
    provider = Provider(
        email=pytest.test_provider_email,
        name="CompanyTEST",
        client_id=pytest.test_provider_client_id,
        client_secret=pytest.test_provider_client_secret,
        wh_secret="wh_$2b$1l5kj8SQH",
        wh_url="http://somesite.com/api/path/webhook/",
    )
    fake_db.add(provider)
    fake_db.commit()


@pytest.fixture(scope="session")
def fake_wallet(fake_db):
    wallet = Wallet(
        email=pytest.test_wallet_email,
        username="CustomerTEST",
        customer_uuid=pytest.test_wallet_customer_uuid,
        debit=Decimal("0.00"),
        credit=Decimal("0.00"),
        balance=pytest.test_wallet_balance,
    )
    fake_db.add(wallet)
    fake_db.commit()


@pytest.fixture(scope="session")
def fake_account(fake_db, fake_provider, fake_wallet):
    account = Account(
        account_number=pytest.test_account_number,
        client_id=pytest.test_provider_client_id,
        owner=pytest.test_wallet_email,
        registered_at=datetime.utcnow(),
        debit=Decimal("0.00"),
        credit=Decimal("0.00"),
        balance=Decimal("0.00"),
    )
    fake_db.add(account)
    fake_db.commit()


@pytest.fixture(scope="session")
def fake_service(fake_db, fake_provider):
    service = Service(
        service_id=pytest.test_provider_service_id,
        client_id=pytest.test_provider_client_id,
        name="Провести тестирование",
        price=pytest.test_provider_service_price,
    )
    fake_db.add(service)
    fake_db.commit()


@pytest.fixture(scope="session")
def test_client():
    client = TestClient(app)
    app.dependency_overrides[get_session] = fake_db_session
    yield client
