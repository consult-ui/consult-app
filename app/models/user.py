from datetime import datetime
from typing import List

from sqlalchemy import (
    BigInteger,
    func,
    Text,
    TIMESTAMP,
    Table,
    ForeignKey,
    Column
)
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.models.base import Base
from app.models.organization import Organization

user_organization_table = Table(
    "user_organizations",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("organization_id", ForeignKey("organizations.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    phone_number: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False)

    password: Mapped[str] = mapped_column(Text, nullable=False)

    first_name: Mapped[str] = mapped_column(Text, nullable=False)
    last_name: Mapped[str] = mapped_column(Text, nullable=False)

    whatsapp_url: Mapped[str] = mapped_column(Text, nullable=False)
    telegram_url: Mapped[str] = mapped_column(Text, nullable=False)

    reset_password_code: Mapped[str] = mapped_column(Text, nullable=True)

    expiration_date: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )

    organizations: Mapped[List[Organization]] = relationship(
        secondary=user_organization_table, lazy="subquery"
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
