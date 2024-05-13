from datetime import datetime, timedelta

import bcrypt
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from jose import JWTError, jwt
from sqlalchemy import select

from src import models
from src.database import async_session, get_session
from src.schemas.company import Company, CompanyLogin
from src.schemas.customer import Customer, CustomerLogin
from src.schemas.token import AccessToken, RefreshToken, Tokens
from src.settings import fast_auth_settings


class AuthService:
    def __init__(self, session: async_session = Depends(get_session)):
        self.session = session

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @classmethod
    def verify_password(cls, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    @classmethod
    def create_access_token(cls, subject_id: str) -> AccessToken:
        now = datetime.utcnow()

        payload = {
            "token_type": "access",
            "iat": now,
            "nbf": now,
            "exp": now + timedelta(seconds=fast_auth_settings.jwt_access_expiration),
            "sub": subject_id,
        }

        access_token = jwt.encode(
            payload,
            fast_auth_settings.jwt_secret,
            algorithm=fast_auth_settings.jwt_algorithm,
        )

        return AccessToken(access=access_token)

    @classmethod
    def create_tokens(cls, subject: Company | Customer) -> Tokens:
        if isinstance(subject, models.Company):
            subject_data = Company.model_validate(subject)
            subject_id = subject_data.client_id
        else:
            subject_data = Customer.model_validate(subject)
            subject_id = subject_data.customer_uuid

        now = datetime.utcnow()

        payload = {
            "token_type": "access",
            "iat": now,
            "nbf": now,
            "exp": now + timedelta(seconds=fast_auth_settings.jwt_access_expiration),
            "sub": subject_id,
        }

        access_token = jwt.encode(
            payload,
            fast_auth_settings.jwt_secret,
            algorithm=fast_auth_settings.jwt_algorithm,
        )

        payload.update(
            {
                "token_type": "refresh",
                "exp": now
                + timedelta(seconds=fast_auth_settings.jwt_refresh_expiration),
            }
        )

        refresh_token = jwt.encode(
            payload,
            fast_auth_settings.jwt_secret,
            algorithm=fast_auth_settings.jwt_algorithm,
        )

        return Tokens(access=access_token, refresh=refresh_token)

    @classmethod
    def validate_token(cls, token: str) -> str:
        token_exception = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(
                token,
                fast_auth_settings.jwt_secret,
                algorithms=[fast_auth_settings.jwt_algorithm],
            )
        except JWTError:
            raise token_exception

        subject_id_data = payload.get("sub")

        token_type = payload.get("token_type")

        if token_type != "refresh":
            raise token_exception

        return subject_id_data

    async def refresh_token(self, refresh_token: RefreshToken) -> AccessToken:
        subject_id = self.validate_token(refresh_token.refresh)

        return self.create_access_token(subject_id)

    async def login(self, login_data: CompanyLogin | CustomerLogin) -> Tokens:
        authentication_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

        if isinstance(login_data, CompanyLogin):
            query = select(models.Company).where(
                models.Company.email == login_data.email
            )
        else:
            query = select(models.Customer).where(
                models.Customer.email == login_data.email
            )

        res = await self.session.execute(query)

        subject = res.scalar()

        if subject is None:
            raise authentication_exception

        if isinstance(login_data, CustomerLogin) and not subject.is_verified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="First time here - all right - we have sent you the verification email.",  # for partner's user
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not self.verify_password(login_data.password, subject.hashed_password):
            raise authentication_exception

        return self.create_tokens(subject)
