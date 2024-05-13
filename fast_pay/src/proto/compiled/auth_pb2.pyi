from typing import ClassVar as _ClassVar
from typing import Optional as _Optional

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message

DESCRIPTOR: _descriptor.FileDescriptor

class SessionRequest(_message.Message):
    __slots__ = ("client_id", "client_secret", "return_url")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    RETURN_URL_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    client_secret: str
    return_url: str
    def __init__(
        self,
        client_id: _Optional[str] = ...,
        client_secret: _Optional[str] = ...,
        return_url: _Optional[str] = ...,
    ) -> None: ...

class SessionResponse(_message.Message):
    __slots__ = ("expire_date", "session_id")
    EXPIRE_DATE_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    expire_date: str
    session_id: str
    def __init__(
        self, expire_date: _Optional[str] = ..., session_id: _Optional[str] = ...
    ) -> None: ...

class CustomerRequest(_message.Message):
    __slots__ = ("email", "username")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    email: str
    username: str
    def __init__(
        self, email: _Optional[str] = ..., username: _Optional[str] = ...
    ) -> None: ...

class CustomerResponse(_message.Message):
    __slots__ = ("customer_uuid",)
    CUSTOMER_UUID_FIELD_NUMBER: _ClassVar[int]
    customer_uuid: str
    def __init__(self, customer_uuid: _Optional[str] = ...) -> None: ...

class AuthCompanyRequest(_message.Message):
    __slots__ = ("client_id", "client_secret")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    client_secret: str
    def __init__(
        self, client_id: _Optional[str] = ..., client_secret: _Optional[str] = ...
    ) -> None: ...

class AuthCompanyResponse(_message.Message):
    __slots__ = ("client_id",)
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    def __init__(self, client_id: _Optional[str] = ...) -> None: ...

class IntrospectRequest(_message.Message):
    __slots__ = ("client_id", "client_secret", "token")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    client_secret: str
    token: str
    def __init__(
        self,
        client_id: _Optional[str] = ...,
        client_secret: _Optional[str] = ...,
        token: _Optional[str] = ...,
    ) -> None: ...

class IntrospectResponse(_message.Message):
    __slots__ = ("scope", "revoked", "checked_at")
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    REVOKED_FIELD_NUMBER: _ClassVar[int]
    CHECKED_AT_FIELD_NUMBER: _ClassVar[int]
    scope: str
    revoked: bool
    checked_at: int
    def __init__(
        self,
        scope: _Optional[str] = ...,
        revoked: bool = ...,
        checked_at: _Optional[int] = ...,
    ) -> None: ...
