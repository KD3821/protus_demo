import pytest

from src.settings import fast_pay_settings


@pytest.mark.usefixtures("fake_provider")
class TestCompanyInfo:
    url = "/companies"

    @pytest.mark.asyncio
    async def test_info(self, test_client):
        response = test_client.get(
            f"{self.url}/info/",
            headers={
                "User": pytest.test_provider_client_id,
                "Authorization": f"{fast_pay_settings.api_key}",
            },
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_dashboard(self, test_client):
        response = test_client.get(
            f"{self.url}/dashboard/",
            headers={
                "User": pytest.test_provider_client_id,
                "Authorization": f"{fast_pay_settings.api_key}",
            },
        )
        assert response.status_code == 200
