import json

import pytest

from src.api.auth import ProxyClient


def test_register_customer(test_client, monkeypatch):
    test_request_payload = {
        "email": pytest.test_customer_email,
        "username": pytest.test_customer_username,
        "password": pytest.test_customer_password,
    }

    test_response_payload = {
        "email": pytest.test_customer_email,
        "username": pytest.test_customer_username,
        "customer_uuid": pytest.test_customer_uuid,
    }

    async def mock_proxy_post_request(*args, **kwargs):
        return test_response_payload

    monkeypatch.setattr(ProxyClient, "proxy_post_request", mock_proxy_post_request)

    response = test_client.post(
        "/auth/register/",
        headers={"User-Type": "customers"},
        content=json.dumps(test_request_payload),
    )

    assert response.status_code == 200
    assert response.json() == test_response_payload


def test_register_customer_invalid_email(test_client):
    test_request_payload = {
        "email": "testcustomermail.com",
        "username": pytest.test_customer_username,
        "password": pytest.test_customer_password,
    }

    response = test_client.post(
        "/auth/register/",
        headers={"User-Type": "customers"},
        content=json.dumps(test_request_payload),
    )

    assert response.status_code == 422


def test_login_customer(test_client, monkeypatch):
    test_request_payload = {
        "email": pytest.test_customer_email,
        "password": pytest.test_customer_password,
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
        headers={"User-Type": "customers"},
        content=json.dumps(test_request_payload),
    )

    assert response.status_code == 200
    assert response.json() == test_response_payload
