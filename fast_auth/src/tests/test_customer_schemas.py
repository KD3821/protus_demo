import json

from src.services.customer_service import CustomerAuthService
from src.settings import fast_auth_settings


def test_register_company(test_client, monkeypatch):
    test_request_payload = {
        "email": "testcustomer@mail.com",
        "username": "John Test",
        "password": "MyTestPassword",
    }

    test_response_payload = {
        "email": "testcustomer@mail.com",
        "username": "John Test",
        "customer_uuid": "1safXjkX2rSySX",
    }

    async def mock_register_customer(service, payload):
        return test_response_payload

    monkeypatch.setattr(
        CustomerAuthService, "register_customer", mock_register_customer
    )

    response = test_client.post(
        "/customers/register/",
        headers={"Authorization": f"{fast_auth_settings.api_key}"},
        content=json.dumps(test_request_payload),
    )

    assert response.status_code == 200
    assert response.json() == test_response_payload


def test_register_customer_invalid_email(test_client):
    test_request_payload = {
        "email": "testcustomermail.com",  # no @
        "username": "John Test",
        "password": "MyTestPassword",
    }

    response = test_client.post(
        "/customers/register/",
        headers={"Authorization": f"{fast_auth_settings.api_key}"},
        content=json.dumps(test_request_payload),
    )

    assert response.status_code == 422


def test_login_customer(test_client, monkeypatch):
    test_request_payload = {
        "email": "testcustomer@mail.com",
        "password": "MyTestPassword",
    }

    test_response_payload = {
        "access": "SuperJwtToken.VerySecured.NoDoubt.Access",
        "refresh": "SuperJwtToken.VerySecured.NoDoubt.Refresh",
    }

    async def mock_login_customer(service, payload):
        return test_response_payload

    monkeypatch.setattr(CustomerAuthService, "login", mock_login_customer)

    response = test_client.post(
        "/customers/login/",
        headers={"Authorization": f"{fast_auth_settings.api_key}"},
        content=json.dumps(test_request_payload),
    )

    assert response.status_code == 200
    assert response.json() == test_response_payload
