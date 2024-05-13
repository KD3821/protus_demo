from decimal import Decimal
from typing import Any, Dict

from pydantic import BaseModel


class BasePayment(BaseModel):
    service_id: str
    user_uuid: str


class PaymentCreate(BasePayment):
    payload: Dict[str, Any] | None


class PaymentCreateResponse(BasePayment):
    invoice_number: str
    issued_at: int  # timestamp
    service_name: str
    amount: Decimal
