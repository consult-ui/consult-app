from datetime import datetime

from pydantic import BaseModel


class PublicUser(BaseModel):
    id: int
    phone_number: str
    email: str
    first_name: str
    last_name: str
    expiration_date: datetime


class ResetPasswordRequest(BaseModel):
    email: str


class ChangePasswordRequest(BaseModel):
    reset_code: str
    new_password: str
