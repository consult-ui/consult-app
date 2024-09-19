from datetime import datetime

from sqlalchemy import (
    func,
    TIMESTAMP,
    BigInteger,
    Text,
    ForeignKey
)
from sqlalchemy.orm import mapped_column, Mapped

from app.db import Base


class Assistant(Base):
    __tablename__ = "assistants"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("chats.id"), nullable=False)

    content: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, default=func.now()
    )

    def __str__(self):
        return self.name
