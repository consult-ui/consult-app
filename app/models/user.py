from sqlalchemy import (
    BigInteger,
    func,
    Text,
    TIMESTAMP,
)
from sqlalchemy.orm import mapped_column, Mapped
from datetime import datetime
from app.db import Base
from app.schemas.base import PydanticType


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    phone_number: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False)

    first_name: Mapped[str] = mapped_column(Text, nullable=False)
    last_name: Mapped[str] = mapped_column(Text, nullable=False)

    expiration_date: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )

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
        return self.email
