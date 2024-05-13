from decimal import Decimal

from pydantic import BaseModel


class WalletInfo(BaseModel):
    username: str
    customer_uuid: str
    balance: Decimal
