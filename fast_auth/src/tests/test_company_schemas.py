import json

from src.services.company_service import CompanyAuthService
from src.settings import fast_auth_settings


def test_register_company(test_client, monkeypatch):
    test_request_payload = {
        "email": "testcompany1@mail.com",
        "name": "TestCo1ANY",
        "password": "MyTestPassword",
    }

    test_response_payload = {
        "email": "testcompany1@mail.com",
        "name": "TestCo1ANY",
        "client_id": "1XX2SSX",
    }

    async def mock_register_company(service, payload):
        return test_response_payload

    monkeypatch.setattr(CompanyAuthService, "register_company", mock_register_company)

    response = test_client.post(
        "/companies/register/",
        headers={"Authorization": f"{fast_auth_settings.api_key}"},
        content=json.dumps(test_request_payload),
    )

    assert response.status_code == 200
    assert response.json() == test_response_payload


def test_register_company_invalid_email(test_client):
    test_request_payload = {
        "email": "testcompany1mail.com",  # no @
        "name": "TestCo1ANY",
        "password": "MyTestPassword",
    }

    response = test_client.post(
        "/companies/register/",
        headers={"Authorization": f"{fast_auth_settings.api_key}"},
        content=json.dumps(test_request_payload),
    )

    assert response.status_code == 422


def test_login_company(test_client, monkeypatch):
    test_request_payload = {
        "email": "testcompany1@mail.com",
        "password": "MyTestPassword",
    }

    test_response_payload = {
        "access": "SuperJwtToken.VerySecured.NoDoubt.Access",
        "refresh": "SuperJwtToken.VerySecured.NoDoubt.Refresh",
    }

    async def mock_login_company(service, payload):
        return test_response_payload

    monkeypatch.setattr(CompanyAuthService, "login", mock_login_company)

    response = test_client.post(
        "/companies/login/",
        headers={"Authorization": f"{fast_auth_settings.api_key}"},
        content=json.dumps(test_request_payload),
    )

    assert response.status_code == 200
    assert response.json() == test_response_payload
