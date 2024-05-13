import pytest

from src.callbacks.wallet import WalletCallbackHandler
from src.settings import fast_pay_settings


@pytest.mark.usefixtures("fake_db")
class TestWallet:
    url = "/customers"
    email = "some_customer@mail.com"
    username = "David Brown"
    customer_uuid = "tdpqsX6dRtYu7QmkSPZ9bc"

    @pytest.mark.asyncio
    async def test_create_provider_from_broker(self, test_client, fake_session_maker):

        callback_handler = WalletCallbackHandler()
        callback_handler.session = fake_session_maker()

        await callback_handler.create_from_broker(
            create_data={
                "email": self.email,
                "username": self.username,
                "customer_uuid": self.customer_uuid,
            }
        )

        provider_res = test_client.get(
            f"{self.url}/info/",
            headers={
                "User": self.customer_uuid,
                "Authorization": f"{fast_pay_settings.api_key}",
            },
        )
        assert provider_res.status_code == 200
