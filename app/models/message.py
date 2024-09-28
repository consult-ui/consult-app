from datetime import datetime
from enum import Enum

from sqlalchemy import (
    func,
    TIMESTAMP,
    BigInteger,
    Text,
    ForeignKey
)
from sqlalchemy.orm import mapped_column, Mapped

from app.models.base import Base


class MessageRole(str, Enum):
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("chats.id"), nullable=False)

    role: Mapped[MessageRole] = mapped_column(Text, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, default=func.now()
    )

    def __str__(self):
        return f"{self.role}:{self.id}"
