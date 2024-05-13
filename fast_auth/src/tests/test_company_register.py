from collections import namedtuple

import pytest

from src.services import company_service
from src.settings import fast_auth_settings


@pytest.mark.usefixtures("fake_db")
class TestCompanyRegister:
    url = "/companies"
    email = "some_company@mail.com"
    name = "Some Name"
    password = "SomePass"

    @pytest.mark.asyncio
    async def test_register_company(self, test_client, monkeypatch):

        async def mock_create_provider_request(service_name, data):
            return {
                "service": "test_payments_service",
                "result": {
                    "id": 1,
                    "email": self.email,
                    "name": self.name,
                },
            }

        MockBroker = namedtuple("MockBroker", ["process_request"])
        mock_broker_handler = MockBroker(mock_create_provider_request)

        monkeypatch.setattr(company_service, "broker_handler", mock_broker_handler)

        register_res = test_client.post(
            f"{self.url}/register/",
            json={
                "email": self.email,
                "name": self.name,
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
