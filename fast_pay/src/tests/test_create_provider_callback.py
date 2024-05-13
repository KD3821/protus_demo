import pytest

from src.callbacks.provider import ProviderCallbackHandler
from src.settings import fast_pay_settings


@pytest.mark.usefixtures("fake_db")
class TestProvider:
    url = "/companies"
    email = "some_company@mail.com"
    name = "SomeName&Co"
    client_id = "JR6IO51W"
    client_secret = "AcE12vkjerPLK78SmSQuapWe"
    wh_secret = "wh_$6n$5k0kj8WTX"

    @pytest.mark.asyncio
    async def test_create_provider_from_broker(self, test_client, fake_session_maker):

        callback_handler = ProviderCallbackHandler()
        callback_handler.session = fake_session_maker()

        await callback_handler.create_from_broker(
            create_data={
                "email": self.email,
                "name": self.name,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "wh_secret": self.wh_secret,
            }
        )

        provider_res = test_client.get(
            f"{self.url}/info/",
            headers={
                "User": self.client_id,
                "Authorization": f"{fast_pay_settings.api_key}",
            },
        )
        assert provider_res.status_code == 200
