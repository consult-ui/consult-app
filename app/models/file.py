import uuid
from datetime import datetime

from sqlalchemy import (
    func,
    TIMESTAMP,
    BigInteger,
    Text,
    ForeignKey,
    UUID
)
from sqlalchemy.orm import mapped_column, Mapped

from app.models.base import Base


class File(Base):
    __tablename__ = "files"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("chats.id"), nullable=False)

    name: Mapped[str] = mapped_column(Text, nullable=False)

    openai_id: Mapped[str] = mapped_column(Text, nullable=False)

    size: Mapped[int] = mapped_column(BigInteger, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
    )

    def __str__(self):
        return self.name
