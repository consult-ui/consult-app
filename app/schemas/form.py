from typing import Optional

from pydantic import BaseModel


class ContactFormRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
