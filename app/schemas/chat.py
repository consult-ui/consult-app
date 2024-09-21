from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UpdateChatRequest(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None


class CreateChatRequest(BaseModel):
    assistant_id: Optional[int] = None


class PublicChat(BaseModel):
    id: int
    name: str
    desc: str
    color: Optional[str] = None
    icon_url: Optional[str] = None
    created_at: datetime
