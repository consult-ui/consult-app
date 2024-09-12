from datetime import datetime

from pydantic import BaseModel, EmailStr


class PublicUser(BaseModel):
    id: int
    phone_number: str
    email: EmailStr
    first_name: str
    last_name: str
    expiration_date: datetime


class ResetPasswordRequest(BaseModel):
    email: EmailStr


class ChangePasswordRequest(BaseModel):
    email: EmailStr
    reset_code: str
    new_password: str
