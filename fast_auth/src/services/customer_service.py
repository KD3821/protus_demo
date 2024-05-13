import shortuuid
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import select

from src import models
from src.broker import broker_handler
from src.logger import logger
from src.schemas.customer import (Customer, CustomerRegister,
                                  PaymentsCustomerRegister)
from src.services import AuthService


class CustomerAuthService(AuthService):

    async def get_unique_cutomer_uuid(self):
        customer_uuid_exists = True

        while customer_uuid_exists:
            customer_uuid_exists = False

            new_customer_uuid = shortuuid.uuid()

            query = select(models.Customer).where(
                models.Customer.customer_uuid == new_customer_uuid
            )

            res = await self.session.execute(query)

            customer_same_uuid = res.scalar()

            if customer_same_uuid:
                customer_uuid_exists = True

        return new_customer_uuid  # noqa    todo refactor -> while - else

    async def get_existing_customer(self, email: str) -> Customer:
        query = select(models.Customer).where(models.Customer.email == email)

        res = await self.session.execute(query)
        existing_customer = res.scalar()

        return existing_customer

    async def verify_existing_customer(
        self, customer: Customer, password: str
    ) -> Customer:
        customer.password = self.hash_password(password)
        customer.is_verified = True

        self.session.add(customer)
        await self.session.commit()

        return customer

    async def register_customer(self, register_data: CustomerRegister) -> Customer:

        customer_exists = await self.get_existing_customer(register_data.email)

        if customer_exists and not customer_exists.is_verified:
            return await self.verify_existing_customer(
                customer_exists, register_data.password
            )

        if customer_exists:
            raise HTTPException(
                detail="Customer already exists. Do you want to reset password?",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        new_customer_uuid = await self.get_unique_cutomer_uuid()

        customer = models.Customer(
            email=register_data.email,
            username=register_data.username,
            hashed_password=self.hash_password(register_data.password),
            customer_uuid=new_customer_uuid,  # noqa
        )

        self.session.add(customer)
        await self.session.commit()

        res = await broker_handler.process_request(
            service_name="payments",
            data={
                "callback": "Wallet.create_from_broker",
                "email": register_data.email,
                "username": register_data.username,
                "customer_uuid": new_customer_uuid,
            },
        )
        service = res.get("service")
        result = res.get("result")

        logger.info(f"*[broker] >> [{service}]* Wallet created: {result}")

        return customer

    async def register_payments_customer(
        self, register_data: PaymentsCustomerRegister
    ) -> Customer:
        customer_exists = await self.get_existing_customer(register_data.email)

        if customer_exists:
            if customer_exists.is_verified:
                logger.info(
                    f"Send notification email about new account to active Protus User: {customer_exists.email}"
                )
            return customer_exists

        new_customer_uuid = await self.get_unique_cutomer_uuid()

        customer = models.Customer(
            email=register_data.email,
            username=register_data.username,
            hashed_password=None,
            customer_uuid=new_customer_uuid,
            is_verified=False,
        )

        self.session.add(customer)
        await self.session.commit()

        return customer
