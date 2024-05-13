from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr


class BaseWallet(BaseModel):
    customer_uuid: str


class WalletCreate(BaseWallet):
    email: EmailStr
    username: str


class Wallet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int


class WalletBalance(BaseWallet):
    balance: Decimal


class WalletInfo(WalletBalance):
    username: str


class WalletByBroker(WalletBalance):
    id: int
    email: EmailStr
