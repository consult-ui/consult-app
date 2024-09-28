from datetime import datetime
from enum import Enum
from typing import TypedDict, Literal, Required, TypeAlias, Union, List

from sqlalchemy import (
    func,
    TIMESTAMP,
    BigInteger,
    ForeignKey,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapped_column, Mapped

from app.models.base import Base


class MessageRole(str, Enum):
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"


class ImageFileParam(TypedDict, total=False):
    file_id: Required[str]
    detail: Literal["auto", "low", "high"]


class ImageFileContentBlockParam(TypedDict, total=False):
    image_file: Required[ImageFileParam]
    type: Required[Literal["image_file"]]


class TextContentBlockParam(TypedDict, total=False):
    text: Required[str]
    type: Required[Literal["text"]]


MessageContentPartParam: TypeAlias = Union[ImageFileContentBlockParam, TextContentBlockParam]


class CodeInterpreterTool(TypedDict, total=False):
    type: Literal["code_interpreter"]


class AttachmentToolAssistantToolsFileSearchTypeOnly(TypedDict, total=False):
    type: Literal["file_search"]


AttachmentTool: TypeAlias = Union[CodeInterpreterTool, AttachmentToolAssistantToolsFileSearchTypeOnly]


class Attachment(TypedDict, total=False):
    file_id: str
    tools: List[AttachmentTool]


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("chats.id"), nullable=False)

    openai_id: Mapped[str] = mapped_column(Text, nullable=False)

    role: Mapped[MessageRole] = mapped_column(Text, nullable=False)
    content: Mapped[List[MessageContentPartParam]] = mapped_column(JSONB, nullable=False)
    attachments: Mapped[List[Attachment]] = mapped_column(JSONB, nullable=False, default=lambda _: [])

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, default=func.now()
    )

    def __str__(self):
        return f"{self.role}:{self.id}"
