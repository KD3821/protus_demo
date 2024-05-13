from typing import ClassVar as _ClassVar
from typing import Optional as _Optional

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message

DESCRIPTOR: _descriptor.FileDescriptor

class AccountRequest(_message.Message):
    __slots__ = ("client_id", "owner")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    owner: str
    def __init__(
        self, client_id: _Optional[str] = ..., owner: _Optional[str] = ...
    ) -> None: ...

class AccountResponse(_message.Message):
    __slots__ = ("account_number",)
    ACCOUNT_NUMBER_FIELD_NUMBER: _ClassVar[int]
    account_number: str
    def __init__(self, account_number: _Optional[str] = ...) -> None: ...

class AccountingRequest(_message.Message):
    __slots__ = ("client_id", "email", "username")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    email: str
    username: str
    def __init__(
        self,
        client_id: _Optional[str] = ...,
        email: _Optional[str] = ...,
        username: _Optional[str] = ...,
    ) -> None: ...

class ChargeRequest(_message.Message):
    __slots__ = ("client_id", "service_id", "account_number")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_NUMBER_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    service_id: str
    account_number: str
    def __init__(
        self,
        client_id: _Optional[str] = ...,
        service_id: _Optional[str] = ...,
        account_number: _Optional[str] = ...,
    ) -> None: ...

class ChargeResponse(_message.Message):
    __slots__ = (
        "service_id",
        "service_name",
        "account_number",
        "invoice_number",
        "issued_at",
        "amount",
    )
    SERVICE_ID_FIELD_NUMBER: _ClassVar[int]
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_NUMBER_FIELD_NUMBER: _ClassVar[int]
    INVOICE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    ISSUED_AT_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    service_id: str
    service_name: str
    account_number: str
    invoice_number: str
    issued_at: int
    amount: float
    def __init__(
        self,
        service_id: _Optional[str] = ...,
        service_name: _Optional[str] = ...,
        account_number: _Optional[str] = ...,
        invoice_number: _Optional[str] = ...,
        issued_at: _Optional[int] = ...,
        amount: _Optional[float] = ...,
    ) -> None: ...
