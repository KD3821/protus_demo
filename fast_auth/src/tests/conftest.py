"""
run tests with command to skip docker-volume:

pytest . --ignore=volumes/db/

"""

import os
from datetime import datetime, timedelta

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
from src.models import Company, Customer, LoginSession

load_dotenv()

pytest.test_company_email = "company_test@mail.com"
pytest.test_company_password = "NewPass"
pytest.test_company_client_id = "D3H6P3WM"
pytest.test_company_client_secret = "lOE54vkjqjPH8F8SqSQuDHPW"

pytest.test_customer_email = "customer_test@mail.com"
pytest.test_customer_password = "NewPass"

pytest.test_login_session_id = "EENTE2XW7ZKZBLO1CU1Z"

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
def fake_company(fake_db):
    company = Company(
        email=pytest.test_company_email,
        name="CompanyTEST",
        hashed_password="$2b$12$S3G2NPjC4/jST6uRyi5CnOLbrdUVveYk97NtNoFWjxNWUgrYkB41i",
        client_id=pytest.test_company_client_id,
        client_secret=pytest.test_company_client_secret,
        wh_secret="wh_$2b$1l5kj8SQH",
        wh_url="http://somesite.com/api/path/webhook/",
    )
    fake_db.add(company)
    fake_db.commit()


@pytest.fixture(scope="session")
def fake_customer(fake_db):
    customer = Customer(
        email=pytest.test_customer_email,
        username="CustomerTEST",
        hashed_password="$2b$12$8jYUB54l1VZYVugr7lY7JeZ25v7MXyFLhbd0MdvXDGYPGo.Ozj.sO",
        customer_uuid="jdtidF6dWfZu7emkSPm7xY",
    )
    fake_db.add(customer)
    fake_db.commit()


@pytest.fixture(scope="session")
def fake_login_session(fake_db):
    login_session = LoginSession(
        client_id=pytest.test_company_client_id,
        email=pytest.test_company_email,
        expire_date=datetime.utcnow() + timedelta(seconds=60),
        session_id=pytest.test_login_session_id,
        return_url="http://anysite.com/any/path/to/",
    )
    fake_db.add(login_session)
    fake_db.commit()


@pytest.fixture(scope="session")
def test_client():
    client = TestClient(app)
    app.dependency_overrides[get_session] = fake_db_session
    yield client
