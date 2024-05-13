from pydantic import BaseModel


class AccessToken(BaseModel):
    access: str


class RefreshToken(BaseModel):
    refresh: str


class Tokens(BaseModel):
    access: str
    refresh: str


class TokenIntrospect(AccessToken):
    client_id: str
    client_secret: str


class TokenIntrospectResult(BaseModel):
    scope: str
    revoked: bool
    checked_at: int
