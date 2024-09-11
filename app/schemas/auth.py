import uuid

from pydantic import BaseModel


class LoginRequest(BaseModel):
    login: str
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: uuid.UUID


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
