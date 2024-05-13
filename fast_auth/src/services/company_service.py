import random
import string

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import and_, or_, select

from src import models
from src.broker import broker_handler
from src.logger import logger
from src.schemas.company import Company, CompanyCLILogin, CompanyRegister
from src.services import AuthService
from src.settings import fast_auth_settings

PAYMENTS_HOST = fast_auth_settings.payments_host
PAYMENTS_PORT = fast_auth_settings.payments_port
API_KEY = fast_auth_settings.api_key


class CompanyAuthService(AuthService):

    async def get_authenticated_company(
        self, auth_data: CompanyCLILogin
    ) -> Company | None:
        query = select(models.Company).where(
            and_(
                models.Company.client_id == auth_data.client_id,
                models.Company.client_secret == auth_data.client_secret,
            )
        )
        res = await self.session.execute(query)

        return res.scalar()

    async def register_company(self, register_data: CompanyRegister) -> Company:
        query = select(models.Company).where(
            or_(
                models.Company.email == register_data.email,
                models.Company.name == register_data.name,
            )
        )

        res = await self.session.execute(query)

        company_exists = res.scalar()

        if company_exists:
            raise HTTPException(
                detail="Company with such name already exist - please use other name.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        client_id_exists = True

        while client_id_exists:
            client_id_exists = False

            new_client_id = "".join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(8)
            )

            query = select(models.Company).where(
                models.Company.client_id == new_client_id
            )

            res = await self.session.execute(query)

            client_same_id = res.scalar()

            if client_same_id:
                client_id_exists = True

        tmp_secret = self.hash_password(
            register_data.password + new_client_id + register_data.name  # noqa
        )
        new_client_secret = tmp_secret[-20:] + new_client_id[::2]

        new_wh_secret = f"wh_{tmp_secret[:5]}{new_client_secret[::3]}"

        company = models.Company(
            email=register_data.email,
            name=register_data.name,
            hashed_password=self.hash_password(register_data.password),
            client_id=new_client_id,
            client_secret=new_client_secret,  # later implement 'show once' logic and hash key before saving to DB
            wh_secret=new_wh_secret,
        )

        self.session.add(company)
        await self.session.commit()

        res = await broker_handler.process_request(
            service_name="payments",  # hard coded
            data={
                "callback": "Provider.create_from_broker",  # hard coded
                "email": register_data.email,
                "name": register_data.name,
                "client_id": new_client_id,
                "client_secret": new_client_secret,
                "wh_secret": new_wh_secret,
            },
        )
        service = res.get("service")
        result = res.get("result")

        logger.info(
            f"*[broker] >> [{service}]* Provider created: "
            f"[ id: {result.get('id')} | email: {result.get('email')} | name: {result.get('name')} ]"
        )

        return company
