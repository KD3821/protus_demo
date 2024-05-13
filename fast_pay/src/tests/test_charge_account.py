import pytest

from src.callbacks.wallet import WalletCallbackHandler
from src.schemas.invoice import InvoiceCreate
from src.services.billing import BillingService
from src.settings import fast_pay_settings


@pytest.mark.usefixtures(
    "fake_db", "fake_account", "fake_provider", "fake_service", "fake_wallet"
)
class TestChargeAccount:
    url = "/customers"

    @pytest.mark.asyncio
    async def test_issue_invoice(self, fake_session_maker):
        test_data = {
            "client_id": pytest.test_provider_client_id,
            "service_id": pytest.test_provider_service_id,
            "account_number": pytest.test_account_number,
        }
        service = BillingService(session=fake_session_maker())

        async with service.session:
            invoice_data = await service.issue_invoice(InvoiceCreate(**test_data))

        assert invoice_data.amount == pytest.test_provider_service_price
        pytest.test_invoice_number = invoice_data.invoice_number

    @pytest.mark.asyncio
    async def test_pay_invoice(self, test_client, fake_session_maker):
        test_data = {
            "invoice_number": pytest.test_invoice_number,
            "payload": {"how": "Pytest only", "why": "Pytest is Awesome"},
        }

        callback_handler = WalletCallbackHandler()
        callback_handler.session = fake_session_maker()

        await callback_handler.pay_invoice_from_broker(invoice_update=test_data)

        billing_res = test_client.get(
            f"{self.url}/dashboard/",
            headers={
                "User": pytest.test_wallet_customer_uuid,
                "Authorization": f"{fast_pay_settings.api_key}",
            },
        )
        assert billing_res.status_code == 200

        operations = billing_res.json().get("operations")

        assert len(operations) >= 1
        assert float(operations[0].get("remaining_balance")) == float(
            pytest.test_wallet_balance - pytest.test_provider_service_price
        )
