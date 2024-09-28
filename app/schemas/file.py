import uuid
from datetime import datetime

from pydantic import BaseModel


class PublicFile(BaseModel):
    id: uuid.UUID
    name: str
    size: int
    created_at: datetime
