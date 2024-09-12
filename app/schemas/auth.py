import uuid

from pydantic import BaseModel


class SignInRequest(BaseModel):
    login: str
    password: str


class SignOutRequest(BaseModel):
    refresh_token: uuid.UUID


class RefreshTokenRequest(BaseModel):
    refresh_token: uuid.UUID


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
