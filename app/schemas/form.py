from typing import Optional

from pydantic import BaseModel, EmailStr


class ContactFormRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
