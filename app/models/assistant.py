from datetime import datetime

from sqlalchemy import (
    func,
    TIMESTAMP,
    BigInteger,
    Text
)
from sqlalchemy.orm import mapped_column, Mapped

from app.db import Base


class Assistant(Base):
    __tablename__ = "assistants"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(Text, nullable=False)
    desc: Mapped[str] = mapped_column(Text, nullable=False, default="")

    color: Mapped[str] = mapped_column(Text, nullable=False)
    icon_url: Mapped[str] = mapped_column(Text, nullable=False)

    instruction: Mapped[str] = mapped_column(Text, nullable=False)

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
