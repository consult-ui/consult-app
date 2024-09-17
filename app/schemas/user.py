from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class PublicUser(BaseModel):
    id: int
    phone_number: str
    email: EmailStr
    first_name: str
    last_name: str
    whatsapp_url: str
    telegram_url: str
    expiration_date: datetime
    organization_id: Optional[int] = None


class ResetPasswordRequest(BaseModel):
    email: EmailStr


class ChangePasswordRequest(BaseModel):
    email: EmailStr
    reset_code: str
    new_password: str
