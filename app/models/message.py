from datetime import datetime
from enum import Enum

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


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)

    openai_id: Mapped[str] = mapped_column(Text, nullable=False)

    role: Mapped[MessageRole] = mapped_column(Text, nullable=False)
    openai_message: Mapped[dict] = mapped_column(JSONB, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, default=func.now()
    )

    def __str__(self):
        return f"{self.role}:{self.id}"
