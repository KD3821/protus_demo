from collections import namedtuple

import pytest

from src.services import oauth_service
from src.settings import fast_auth_settings


@pytest.mark.usefixtures("fake_login_session")
class TestOAuthSession:
    url = "/oauth-widget"

    @pytest.mark.asyncio
    async def test_finalize_oauth_login(self, test_client, monkeypatch):

        async def mock_get_account_number(client_id, email):
            return "12SomEaCcoUNtNuMbEr12"

        async def mock_trigger_webhook(**payload):
            Resp = namedtuple("Resp", ["status_code"])
            resp = Resp(201)
            return resp

        monkeypatch.setattr(
            oauth_service, "get_account_number", mock_get_account_number
        )
        monkeypatch.setattr(oauth_service, "trigger_webhook", mock_trigger_webhook)

        response = test_client.post(
            f"{self.url}/login/",
            json={
                "email": pytest.test_customer_email,
                "password": pytest.test_customer_password,
                "session_id": pytest.test_login_session_id,
                "scope": ["test_check", "test_hold", "test_charge"],
            },
            headers={"Authorization": f"{fast_auth_settings.api_key}"},
        )
        assert response.status_code == 200
