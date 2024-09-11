from datetime import datetime

from pydantic import BaseModel


class PublicUser(BaseModel):
    id: int
    phone_number: str
    email: str
    first_name: str
    last_name: str
    expiration_date: datetime
