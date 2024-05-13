import pytest
from starlette.testclient import TestClient

from src.main import app

pytest.test_company_email = "testcompany@mail.com"
pytest.test_company_name = "Test & Co"
pytest.test_company_password = "TestPassword"
pytest.test_company_client_id = "1XX2SSX"

pytest.test_customer_email = "testcustomer@mail.com"
pytest.test_customer_username = "John Doe"
pytest.test_customer_password = "TestPassword"
pytest.test_customer_uuid = "jdtidF6dWfZu7emkSPm7xY"


@pytest.fixture(scope="session")
def test_client():
    client = TestClient(app)
    yield client
