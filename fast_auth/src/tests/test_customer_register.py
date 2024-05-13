from collections import namedtuple

import pytest

from src.services import customer_service
from src.settings import fast_auth_settings


@pytest.mark.usefixtures("fake_db")
class TestCustomerRegister:
    url = "/customers"
    email = "some_customer@mail.com"
    username = "John Doe"
    password = "SomePass"

    @pytest.mark.asyncio
    async def test_register_customer(self, test_client, monkeypatch):

        async def mock_create_wallet_request(service_name, data):
            return {"service": "test_payments_service", "result": "create_wallet_json"}

        MockBroker = namedtuple("MockBroker", ["process_request"])
        mock_broker_handler = MockBroker(mock_create_wallet_request)

        monkeypatch.setattr(customer_service, "broker_handler", mock_broker_handler)

        register_res = test_client.post(
            f"{self.url}/register/",
            json={
                "email": self.email,
                "username": self.username,
                "password": self.password,
            },
            headers={"Authorization": f"{fast_auth_settings.api_key}"},
        )
        assert register_res.status_code == 200

        login_res = test_client.post(
            f"{self.url}/login/",
            json={"email": self.email, "password": self.password},
            headers={"Authorization": f"{fast_auth_settings.api_key}"},
        )
        assert login_res.status_code == 200
