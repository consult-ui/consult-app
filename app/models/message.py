from datetime import datetime
from enum import Enum

from openai.types.beta.threads.message import Message as OpenaiMessage
from sqlalchemy import (
    func,
    TIMESTAMP,
    BigInteger,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import mapped_column, Mapped

from app.models.base import Base
from app.schemas.base import PydanticType


class MessageRole(str, Enum):
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("chats.id"), nullable=False)

    openai_id: Mapped[str] = mapped_column(Text, nullable=False)

    role: Mapped[MessageRole] = mapped_column(Text, nullable=False)
    openai_msg: Mapped[OpenaiMessage] = mapped_column(PydanticType(OpenaiMessage), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, default=func.now()
    )

    def __str__(self):
        return f"{self.role}:{self.id}"
