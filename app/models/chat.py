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


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    organization_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("organizations.id"), nullable=True)

    name: Mapped[str] = mapped_column(Text, nullable=False)
    desc: Mapped[str] = mapped_column(Text, nullable=False, default="")

    color: Mapped[str] = mapped_column(Text, nullable=True)
    icon_url: Mapped[str] = mapped_column(Text, nullable=True)

    system_prompt: Mapped[str] = mapped_column(Text, nullable=False)

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
