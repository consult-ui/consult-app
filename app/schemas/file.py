from datetime import datetime

from pydantic import BaseModel


class PublicFile(BaseModel):
    id: str
    name: str
    size: int
    created_at: datetime


class DeleteFileRequest(BaseModel):
    file_id: str
