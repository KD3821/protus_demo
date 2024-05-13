from sqlalchemy import select

from src import models
from src.database import async_session
from src.schemas.provider import ProviderByBroker, ProviderCreate


class ProviderCallbackHandler:
    def __init__(self):
        self.session = async_session()

    async def create_from_broker(self, create_data: dict) -> dict:
        valid_data = ProviderCreate.model_validate(create_data)

        async with self.session:
            query = select(models.Provider).where(
                models.Provider.client_id == valid_data.client_id
            )

            res = await self.session.execute(query)

            provider_exists = res.scalar()

            if provider_exists:
                exists = ProviderByBroker(
                    id=provider_exists.id,
                    email=provider_exists.email,
                    name=provider_exists.name,
                )
                return (
                    exists.model_dump()
                )  # in case same message in broker_queue - same data reply to ack

            provider = models.Provider(
                email=valid_data.email,
                name=valid_data.name,
                client_id=valid_data.client_id,
                client_secret=valid_data.client_secret,
                wh_secret=valid_data.wh_secret,
            )

            self.session.add(provider)
            await self.session.commit()

            provider_created = ProviderByBroker(
                id=provider.id, email=provider.email, name=provider.name
            )

            return provider_created.model_dump()
