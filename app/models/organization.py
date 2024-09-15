from datetime import datetime

from sqlalchemy import (
    func,
    TIMESTAMP,
    BigInteger,
    Text
)
from sqlalchemy.orm import mapped_column, Mapped

from app.db import Base


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(Text, nullable=False)
    activity_type: Mapped[str] = mapped_column(Text, nullable=False)

    tax_number: Mapped[str] = mapped_column(Text, nullable=True)
    head_name: Mapped[str] = mapped_column(Text, nullable=True)
    address: Mapped[str] = mapped_column(Text, nullable=True)

    quarterly_income: Mapped[int] = mapped_column(BigInteger, nullable=True)
    quarterly_expenses: Mapped[int] = mapped_column(BigInteger, nullable=True)
    number_employees: Mapped[int] = mapped_column(BigInteger, nullable=True)
    average_receipt: Mapped[int] = mapped_column(BigInteger, nullable=True)

    context: Mapped[str] = mapped_column(Text, nullable=False, default="")

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
