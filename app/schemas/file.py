import uuid
from datetime import datetime

from pydantic import BaseModel


class PublicFile(BaseModel):
    id: uuid.UUID
    name: str
    size: int
    created_at: datetime


class DeleteFileRequest(BaseModel):
    file_id: uuid.UUID
