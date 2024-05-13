import json

import pytest

from src.settings import fast_auth_settings


@pytest.mark.usefixtures("fake_customer")
class TestCustomerAuth:
    url = "/customers"

    @pytest.mark.asyncio
    async def test_login(self, test_client):
        response = test_client.post(
            f"{self.url}/login/",
            json={
                "email": pytest.test_customer_email,
                "password": pytest.test_customer_password,
            },
            headers={"Authorization": f"{fast_auth_settings.api_key}"},
        )
        assert response.status_code == 200
        pytest.test_access_token = response.json().get("access")
        pytest.test_refresh_token = response.json().get("refresh")

    @pytest.mark.asyncio
    async def test_refresh(self, test_client):
        response = test_client.post(
            f"{self.url}/refresh/",
            content=json.dumps({"refresh": pytest.test_refresh_token}),
            headers={"Authorization": f"{fast_auth_settings.api_key}"},
        )
        assert response.status_code == 200
        pytest.test_access_token = response.json().get("access")
