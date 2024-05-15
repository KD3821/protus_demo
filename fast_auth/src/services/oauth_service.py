import random
import string
from datetime import datetime, timedelta
from typing import List

from fastapi import status
from fastapi.exceptions import HTTPException
from jose import jwt
from sqlalchemy import and_, select

from src import models
from src.proto.handlers.accounts import get_account_number
from src.schemas.company import Company
from src.schemas.customer import Customer
from src.schemas.session import (CompletedLoginSession, LoginSessionID,
                                 LoginSessionRequest, LoginSessionResponse,
                                 OAuthCustomerLogin, OAuthToken,
                                 StartedLoginSession)
from src.schemas.token import TokenIntrospect, TokenIntrospectResult
from src.services import AuthService
from src.settings import fast_auth_settings
from src.triggers import trigger_webhook


class OAuthService(AuthService):

    async def get_company(self, client_id: str) -> Company:
        query = select(models.Company).where(models.Company.client_id == client_id)

        res = await self.session.execute(query)

        company = res.scalar()

        return company

    async def create_oauth_access_token(
        self,
        customer: Customer,
        company: Company,
        scope: List[str],
        account_number: str,
    ) -> OAuthToken:
        now = datetime.utcnow()

        exp = now + timedelta(seconds=fast_auth_settings.jwt_access_expiration)

        payload = {
            "token_type": "access",
            "iat": now,
            "nbf": now,
            "exp": exp,
            "sub": account_number,
        }

        new_scope = " ".join(scope)
        payload.update({"scope": new_scope})

        oauth_access_token = jwt.encode(
            payload,
            company.client_secret,
            algorithm=fast_auth_settings.jwt_algorithm,
        )

        new_oauth_token = models.OAuthToken(
            client_id=company.client_id,
            email=customer.email,
            refresh=False,  # in future API versions 'Refresh' Token may be needed
            scope=new_scope,
            token=oauth_access_token,
            expire_date=exp,
        )

        self.session.add(new_oauth_token)
        await self.session.commit()

        return OAuthToken(access=oauth_access_token)

    async def validate_credentials(self, client_id: str, client_secret: str) -> Company:
        authentication_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid CLI credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        query = select(models.Company).where(
            and_(
                models.Company.client_id == client_id,
                models.Company.client_secret == client_secret,
            )
        )

        res = await self.session.execute(query)

        company = res.scalar()

        if company is None:
            raise authentication_exception

        return company

    async def create_login_session(
        self, data: LoginSessionRequest
    ) -> LoginSessionResponse:
        company = await self.validate_credentials(data.client_id, data.client_secret)

        session_id = "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(20)
        )

        login_session = models.LoginSession(
            client_id=company.client_id,
            expire_date=datetime.utcnow() + timedelta(seconds=60),
            session_id=session_id,  # todo make 100% unique
            return_url=data.return_url,
        )

        self.session.add(login_session)
        await self.session.commit()

        return LoginSessionResponse(
            session_id=login_session.session_id, expire_date=login_session.expire_date
        )

    async def get_oauth_session(self, session_id: str) -> models.LoginSession:
        session_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Login Session",
            headers={"WWW-Authenticate": "Bearer"},
        )

        query = select(models.LoginSession).where(
            and_(
                models.LoginSession.session_id == session_id,
                models.LoginSession.confirmation_id == None,  # noqa
            )
        )

        res = await self.session.execute(query)

        session = res.scalar()

        if session is None or session.expire_date <= datetime.utcnow():
            raise session_exception

        return session

    async def start_oauth_session(
        self, session_data: LoginSessionID
    ) -> StartedLoginSession:
        oauth_session = await self.get_oauth_session(session_data.session_id)

        company = await self.get_company(oauth_session.client_id)

        return StartedLoginSession(
            company_name=company.name, return_url=oauth_session.return_url
        )

    async def finalize_oauth_session(
        self, login_data: OAuthCustomerLogin
    ) -> CompletedLoginSession:
        authentication_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

        query = select(models.Customer).where(models.Customer.email == login_data.email)

        res = await self.session.execute(query)

        customer = res.scalar()

        if customer is None:
            raise authentication_exception

        if not customer.is_verified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="First time here - all right - we have sent you the verification email.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not self.verify_password(login_data.password, customer.hashed_password):
            raise authentication_exception

        oauth_session = await self.get_oauth_session(login_data.session_id)

        company = await self.get_company(oauth_session.client_id)

        account_number = await get_account_number(company.client_id, customer.email)

        new_token = await self.create_oauth_access_token(
            customer, company, login_data.scope, account_number
        )

        now = datetime.utcnow()

        confirmation_id = "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(10)
        )

        oauth_session.finalized_at = now
        oauth_session.email = customer.email
        oauth_session.confirmation_id = confirmation_id

        self.session.add(oauth_session)
        await self.session.commit()

        webhook_data = {
            "access": new_token.access,
            "email": customer.email,
            "username": customer.username,
            "finalized_at": str(now),
            "session_id": oauth_session.session_id,
            "confirmation_id": confirmation_id,
        }

        res = await trigger_webhook(
            url=f"http://{fast_auth_settings.demo_host}:{fast_auth_settings.demo_port}{company.wh_url}",  # company.wh_url
            data=webhook_data,
            wh_secret=company.wh_secret,
            user_type="oauth-access",
        )

        if res.status_code != 201:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Connection Error",
            )

        completed_session = CompletedLoginSession(
            return_url=f"{oauth_session.return_url}?cid={confirmation_id}"
        )

        return completed_session

    async def introspect_token(
        self, token_data: TokenIntrospect
    ) -> TokenIntrospectResult:
        company = await self.validate_credentials(
            token_data.client_id, token_data.client_secret
        )

        now = datetime.utcnow()

        query = select(models.OAuthToken).where(
            and_(
                models.OAuthToken.client_id == company.client_id,
                models.OAuthToken.token == token_data.access,
                models.OAuthToken.expire_date > now,
            )
        )

        res = await self.session.execute(query)

        token = res.scalar()

        return TokenIntrospectResult(
            scope=token.scope, revoked=token.revoked, checked_at=int(now.timestamp())
        )
