from datetime import datetime
from enum import Enum
from typing import Any
from typing import Optional, List, Literal, TypeAlias, Union

from openai import AsyncOpenAI
from openai.types.beta.threads.message import MessageContent
from pydantic import BaseModel

from app.config import settings

openai_client = AsyncOpenAI(api_key=settings.openai_api_key)


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


class ImageFileParam(BaseModel):
    file_id: str


class ImageFileContentBlockParam(BaseModel):
    image_file: ImageFileParam
    type: Literal["image_file"]


class TextContentBlockParam(BaseModel):
    text: str
    type: Literal["text"]


MessageContentPartParam: TypeAlias = Union[ImageFileContentBlockParam, TextContentBlockParam]


class SendMessageRequest(BaseModel):
    content: List[MessageContentPartParam]
    attachments: List[str]


class EventType(str, Enum):
    TEXT_DONE = "text_done"
    TEXT_DELTA = "text_delta"
    TEXT_CREATED = "text_created"
    MESSAGE_DONE = "message_done"


class Event(BaseModel):
    type: EventType
    payload: Any


class PulicAttachment(BaseModel):
    file_id: Optional[str] = None


class PublicMessage(BaseModel):
    id: str
    attachments: Optional[List[PulicAttachment]] = None
    content: List[MessageContent]
    created_at: int
    role: Literal["user", "assistant"]
    status: Optional[Literal["in_progress", "incomplete", "completed"]] = None


class ChatQuestions(BaseModel):
    questions: List[str]
