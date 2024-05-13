from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel, ConfigDict


class BaseOperation(BaseModel):
    invoice_number: str
    service_id: str
    date: datetime
    amount: Decimal


class OperationCreate(BaseOperation):
    reference_code: str
    account_number: str
    remaining_balance: Decimal


class Operation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int


class OperationService(BaseModel):
    date: datetime
    service_name: str
    provider_name: str
    reference_code: str
    invoice_number: str
    amount: Decimal
    remaining_balance: Decimal
