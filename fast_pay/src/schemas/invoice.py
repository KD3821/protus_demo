from typing import Any, Dict

from pydantic import BaseModel, ConfigDict


class InvoiceCreate(BaseModel):
    client_id: str
    service_id: str
    account_number: str


class Invoice(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int


class InvoiceUpdate(BaseModel):
    invoice_number: str
    payload: Dict[str, Any] | None
