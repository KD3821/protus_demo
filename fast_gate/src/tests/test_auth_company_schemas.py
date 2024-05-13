import json

import pytest

from src.api.auth import ProxyClient


def test_register_company(test_client, monkeypatch):
    test_request_payload = {
        "email": pytest.test_company_email,
        "name": pytest.test_company_name,
        "password": pytest.test_company_password,
    }

    test_response_payload = {
        "email": pytest.test_company_email,
        "name": pytest.test_company_name,
        "client_id": pytest.test_company_client_id,
    }

    async def mock_proxy_post_request(*args, **kwargs):
        return test_response_payload

    monkeypatch.setattr(ProxyClient, "proxy_post_request", mock_proxy_post_request)

    response = test_client.post(
        "/auth/register/",
        headers={"User-Type": "companies"},
        content=json.dumps(test_request_payload),
    )

    assert response.status_code == 200
    assert response.json() == test_response_payload


def test_register_company_invalid_email(test_client):
    test_request_payload = {
        "email": "testcompanymail.com",
        "name": pytest.test_company_name,
        "password": pytest.test_company_password,
    }

    response = test_client.post(
        "/auth/register/",
        headers={"User-Type": "companies"},
        content=json.dumps(test_request_payload),
    )

    assert response.status_code == 422


def test_login_company(test_client, monkeypatch):
    test_request_payload = {
        "email": pytest.test_company_email,
        "password": pytest.test_company_password,
    }

    test_response_payload = {
        "access": "SuperJwtToken.VerySecured.NoDoubt.Access",
        "refresh": "SuperJwtToken.VerySecured.NoDoubt.Refresh",
    }

    async def mock_proxy_post_request(*args, **kwargs):
        return test_response_payload

    monkeypatch.setattr(ProxyClient, "proxy_post_request", mock_proxy_post_request)

    response = test_client.post(
        "/auth/login/",
        headers={"User-Type": "companies"},
        content=json.dumps(test_request_payload),
    )

    assert response.status_code == 200
    assert response.json() == test_response_payload
