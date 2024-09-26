from typing import Optional

from pydantic import BaseModel, EmailStr


class ContactFormRequest(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
