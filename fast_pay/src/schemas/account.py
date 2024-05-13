from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr


class BaseAccount(BaseModel):
    client_id: str


class AccountCreate(BaseAccount):
    owner: EmailStr


class Account(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int


class AccountingCreate(BaseModel):
    client_id: str
    email: EmailStr
    username: str


class AccountInfo(BaseModel):
    account_number: str
    registered_at: datetime
    balance: Decimal


class AccountInfoCompany(AccountInfo):
    owner: EmailStr


class AccountInfoCustomer(AccountInfo):
    company_name: str
